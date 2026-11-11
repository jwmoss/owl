# AGENTS.md

Ansible playbooks that set up an AMD Strix Halo machine (Ryzen AI Max+ 395, 128 GB, Ubuntu Server 26.04)
with ROCm and local LLM engines. Read [README.md](README.md) first.

**To set up a machine for the user, follow the `owl-setup` skill:**
[.agents/skills/owl-setup/SKILL.md](.agents/skills/owl-setup/SKILL.md).

## Layout

| Path | Holds |
|------|-------|
| `ansible/inventory/group_vars/all.yml` | All settings and version pins |
| `ansible/inventory/hosts.yml` | The user's machine (gitignored; copy `hosts.example.yml`) |
| `ansible/inventory/host_vars/<host>.yml` | Per-machine overrides (gitignored) |
| `ansible/ubuntu.yml` | Base packages, sudo, groups, ROCm, GPU memory limit (reboots once) |
| `ansible/<engine>.yml`, `ansible/roles/<engine>/` | One engine: download, systemd unit, start |
| `ansible/test.yml` | Starts each installed engine and checks one chat answer |
| `docs/` | Install, ROCm and engine details |

Run all Ansible commands from `ansible/`.

## Rules

- Never delete anything under `~/Models` on the machine. The models are hundreds of GB.
  A download that stops resumes when you run the playbook again.
- Only one engine runs at a time. Switch with `sudo systemctl start <service>`; the units conflict.
- Do not use `pkill -f <pattern>` over SSH. The pattern matches your own SSH command and kills it.
  Use `systemctl stop`, or a bracket pattern such as `pkill -f "[a]ria2c"`.
- Do not commit the user's address, user name, tokens or host_vars. Those files are gitignored.
- Do not install or host a model that the user's license territory excludes. Read the model's license first.

## Change the code

- Keep each role in the same shape: a pinned download, a unit with `Conflicts=` for the other engines,
  `ExecStartPre=/usr/local/bin/owl-wait-memory`, `RestartSec=30`, and a restart of the default engine
  when its unit changes.
- Pin every version: a commit, a release tag, an image tag or a Hugging Face revision. Check a SHA-256 when the source gives one.
- Put Jinja at the end of a task name (ansible-lint `name[template]`).
- Write docs in ASD-STE100 Simplified Technical English: active voice, present tense, short sentences.
- Use conventional commits. release-please makes the version from them: `fix:` is a patch, `feat:` is a minor
  release, and `feat!:` or a `BREAKING CHANGE:` footer is a major release. An engine version bump is `feat:`.
- Lint before you commit: `cd ansible && uvx ansible-lint --exclude .collections`.
- Test on a machine: `ansible-playbook test.yml` (all installed engines) or `-e '{"engines": ["halogen"]}'`.
