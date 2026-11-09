# owl — local AI server

`owl` is a GMKtec EVO-X2 mini PC that runs large language models on the local network.
This repository records how the machine is set up, so that you can rebuild it.

## Status

| Step | State |
|------|-------|
| PXE boot through netboot.xyz | Done |
| Ubuntu Server 26.04 LTS install | Done |
| Passwordless `sudo` for `jwmoss` | Done |
| ROCm 7.14.1 (TheRock, gfx1151) | Done |
| `ttm` GPU memory limit | Done, active after reboot |
| BIOS: UMA frame buffer at minimum (2 GB) | Done |
| Strata + Qwen3.8-Flash-Next (systemd, port 8080) | Done |
| libosmos + DeepSeek-V4.1-Flash | Playbook runs, download in progress |
| gufo + Qwen3.8-Flash-Next | Playbook runs, download in progress |
| halogen + Qwen3.8-Flash-Next | Playbook runs, download in progress |
| Project Maya + DeepSeek Maya-XS | Setup in progress, service not written yet |
| End-to-end test (`test.yml`) | Passes for Strata |
| UniFi DHCP reservation for `owl` | To do |

## Machine

| Item | Value |
|------|-------|
| Hostname | `owl` |
| Model | GMKtec EVO-X2 (NucBox_EVO-X2) |
| CPU / GPU | AMD Ryzen AI Max+ 395, Radeon 8060S (`gfx1151`, PCI `1002:1586`) |
| Memory | 128 GB LPDDR5X, shared by the CPU and the GPU |
| Disk | 2 TB Crucial E100 NVMe (`CT2000E100SSD8`), one ext4 root filesystem |
| OS | Ubuntu Server 26.04 LTS, kernel 7.0 |
| User | `jwmoss`, SSH key imported from GitHub, password login over SSH off |

## Network

| Item | Value |
|------|-------|
| IP address | `192.168.1.241` (DHCP, Default network) |
| MAC (`eno1`) | `84:47:09:9a:42:3c` |
| Switch port | Office Switch (US-24-PoE 250W), port 8, native network Default |
| SSH | `ssh jwmoss@192.168.1.241` |

## Documents

1. [Network boot with netboot.xyz](docs/01-netboot.md)
2. [Ubuntu install](docs/02-ubuntu-install.md)
3. [ROCm and GPU memory](docs/03-rocm.md)
4. [Inference engines and models](docs/04-models.md)

## Redeploy with Ansible

The playbook in [`ansible/`](ansible/) sets up a fresh Ubuntu Server 26.04 install:
build tools, ROCm, the GPU memory limit and the engines. Each part has its own playbook:

| Playbook | Does |
|----------|------|
| `ubuntu.yml` | Build tools, passwordless sudo, GPU groups, Hugging Face CLI and token, ROCm, `ttm` limit |
| `strata.yml` | Strata with Qwen3.8-Flash-Next |
| `gufo.yml` | gufo with Qwen3.8-Flash-Next |
| `libosmos.yml` | libosmos with DeepSeek-V4.1-Flash |
| `halogen.yml` | halogen with Qwen3.8-Flash-Next |
| `maya.yml` | Project Maya with DeepSeek-V4.1-Flash (setup only) |
| `test.yml` | End-to-end test of each engine |
| `site.yml` | All of the above |

Do these steps by hand first. Ansible cannot do them:

1. Install Ubuntu (see [docs/02-ubuntu-install.md](docs/02-ubuntu-install.md)).
2. Allow passwordless sudo one time (same document).
3. In the BIOS, set **UMA Frame Buffer Size** to the minimum (2 GB on `owl`).

Then run from your Mac:

```sh
cd ansible
uvx --from ansible-core==2.22.0 ansible-galaxy collection install -r requirements.yml
uvx --from ansible-core==2.22.0 ansible-playbook site.yml   # or one playbook, e.g. strata.yml
```

The first run downloads about 545 GB of models. The token in `~/.cache/huggingface/token` on your Mac is copied to `owl`; without it, downloads are slow.
To change the engine that starts at boot, set `default_engine` in
[`inventory/host_vars/owl.yml`](ansible/inventory/host_vars/owl.yml).
