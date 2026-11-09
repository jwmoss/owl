# owl

Ansible playbooks that set up an AMD Strix Halo machine (Ryzen AI Max+ 395, 128 GB) to run large language models.
They install ROCm and one or more inference engines on Ubuntu Server 26.04 LTS. Each engine serves an
OpenAI-compatible API on your network.

Tested on a GMKtec EVO-X2 with 128 GB.

## Engines

| Engine | Model | Port | Playbook |
|--------|-------|------|----------|
| [halogen](https://github.com/peonist-ai/halogen-flash-server) (default) | Qwen3.8-Flash-Next | 8731 | `halogen.yml` |
| [Strata](https://github.com/Niko1221/Strata) | Qwen3.8-Flash-Next | 8080 | `strata.yml` |
| [gufo](https://github.com/gufo-org/gufo) | Qwen3.8-Flash-Next | 8081 | `gufo.yml` |
| [libosmos](https://github.com/mrsirg97-rgb/libosmos) | DeepSeek-V4.1-Flash, abliterated | 8091 | `libosmos.yml` |
| [Project Maya](https://github.com/mw00/project-maya) | DeepSeek-V4.1-Flash | 8099 | `maya.yml` |

Each engine uses almost all of the memory, so only one runs at a time. See [docs/03-engines.md](docs/03-engines.md).

## Quick start

1. Install Ubuntu Server 26.04 LTS, set the BIOS frame buffer to the minimum and allow passwordless sudo.
   See [docs/01-ubuntu-install.md](docs/01-ubuntu-install.md).
2. On your computer, install Ansible and the collections:

   ```sh
   uv tool install ansible-core
   cd ansible
   ansible-galaxy collection install -r requirements.yml
   ```

3. Copy `inventory/hosts.example.yml` to `inventory/hosts.yml`. Set your machine's address and user.
4. Optional: run `hf auth login` on your computer. Ansible copies the token, and downloads are faster.
5. Set up Ubuntu and halogen (about 120 GB of downloads), then test it:

   ```sh
   ansible-playbook ubuntu.yml halogen.yml
   ansible-playbook test.yml -e '{"engines": ["halogen"]}'
   ```

   `ubuntu.yml` reboots the machine one time to apply the GPU memory limit.

6. Check the API:

   ```sh
   curl http://<host>:8731/health
   ```

## Playbooks

| Playbook | Does |
|----------|------|
| `ubuntu.yml` | Build tools, passwordless sudo, GPU groups, Hugging Face CLI, ROCm, GPU memory limit |
| `<engine>.yml` | One engine, its model and its systemd service |
| `site.yml` | `ubuntu.yml` and all engines (about 900 GB of downloads) |
| `test.yml` | Starts each engine, sends one chat request and checks the answer |

Settings, such as the engine that starts at boot (`default_engine`), are in
[`ansible/inventory/group_vars/all.yml`](ansible/inventory/group_vars/all.yml).

## Documents

1. [Ubuntu install](docs/01-ubuntu-install.md)
2. [ROCm and GPU memory](docs/02-rocm.md)
3. [Inference engines and models](docs/03-engines.md)
