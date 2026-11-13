---
name: owl-setup
description: Set up an AMD Strix Halo machine (Ryzen AI Max+ 395, 128 GB) with ROCm and a local LLM engine from this repository, then test it and connect a client. Use when the user wants to install, configure, update or troubleshoot owl on their own machine, or asks to "set up my Strix Halo".
---

# owl setup

You run Ansible from the user's computer (the controller) against their Strix Halo machine (the host) over SSH.
The playbooks do the work. Your job: collect four values, check the preconditions, run the playbooks, and report.

## 1. Ask the user

Ask only for what you cannot find. Use these defaults when the user has no preference.

| Value | Default |
|-------|---------|
| Host address (IP or DNS name) | none: ask |
| SSH user on the host | none: ask |
| Engine | `halogen` (fastest Qwen3.8-Flash-Next; about 120 GB of downloads) |
| Abliterated model (`halogen_abliterated` or `gufo_abliterated`) | `false` |

The other engines are in [docs/03-engines.md](../../../docs/03-engines.md). `site.yml` installs all of them (about 900 GB).

## 2. Steps only the user can do

Check each one. If one is not done, tell the user what to do, and wait.

1. **BIOS:** UMA frame buffer at its minimum, Secure Boot off. See [docs/01-ubuntu-install.md](../../../docs/01-ubuntu-install.md).
2. **Ubuntu Server 26.04 LTS** on the whole disk, with OpenSSH and the user's SSH key.
3. **SSH with a key:** `ssh -o BatchMode=yes <user>@<host> true` must succeed.
4. **Passwordless sudo:** `ssh <user>@<host> sudo -n true` must succeed. If it fails, the user must run this
   in their own terminal, because it asks for the password:

   ```sh
   ssh -t <user>@<host> 'echo "<user> ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/90-<user> && sudo chmod 440 /etc/sudoers.d/90-<user>'
   ```

Optional but recommended: the user runs `hf auth login` on the controller. Ansible copies the token,
and Hugging Face throttles anonymous downloads.

## 3. Prepare the controller

From the repository root:

```sh
command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh
cd ansible
uvx --from ansible-core ansible-galaxy collection install -r requirements.yml
```

Write `ansible/inventory/hosts.yml` (gitignored) from `hosts.example.yml`:

```yaml
all:
  hosts:
    strix:
      ansible_host: <host>
      ansible_user: <user>
```

Write settings that differ from `group_vars/all.yml` to `ansible/inventory/host_vars/strix.yml` (gitignored),
for example `default_engine: gufo` or `halogen_abliterated: true`. Do not edit `group_vars/all.yml` for one machine.

Check: `uvx --from ansible-core ansible all -m ping` answers `pong`.

## 4. Run the playbooks

Run each one from `ansible/` with `uvx --from ansible-core ansible-playbook <file>`.

1. `ubuntu.yml`: base packages, ROCm, GPU memory limit. It reboots the host one time. About 15 minutes.
2. `<engine>.yml`: the engine, its model and its service. The model download takes from 30 minutes to some hours.
   Run it in the background and write its output to a log, so your session does not time out.
   Check the log every few minutes. If it stops, run it again: downloads resume and checksums are checked.
3. `test.yml -e '{"engines": ["<engine>"]}'`: starts the engine and checks one answer.
   Success looks like `<engine> (<model id>) answered 51`.

A second run of any playbook must show `changed=0` (or only the download checks). Use that as the proof of a clean install.

## 5. Report to the user

Give them:

- The API: `http://<host>:<port>/v1` (ports: halogen 8731, Strata 8080, gufo 8081, libosmos 8091, Maya 8099).
- The model id from `curl http://<host>:<port>/v1/models`.
- How to switch engines: `ssh <user>@<host> sudo systemctl start <service>`.
- The pi client example in [docs/03-engines.md](../../../docs/03-engines.md#use-with-pi), if they use pi.
- That the APIs have no key (except Strata), so the host must stay on a trusted network.

## Troubleshooting

| Symptom | Cause and fix |
|---------|---------------|
| `ubuntu.yml` stops at "Check that Linux sees about 128 GB" | The BIOS frame buffer is too large. The user sets it to the minimum. |
| `rocminfo` does not show `gfx1151` | Not a Strix Halo, or the reboot did not happen. Reboot, then run `ubuntu.yml` again. |
| A download is slow or stops | Run the playbook again (it resumes). Ask the user for `hf auth login` if they have no token. |
| The engine restarts again and again | `journalctl -u <service> -n 100`. Usually low memory: stop the other engines. |
| A rootless Podman engine fails after logout | `loginctl show-user <user> -p Linger` must be `yes`. Run `ubuntu.yml` again. |
| The first answer in a long chat is slow after a restart | Expected: the engine reads the whole history again (about 1,900 tokens/s). |

Never delete `~/models` on the host to fix a problem. Ask the user first.
