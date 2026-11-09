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
| BIOS: set UMA frame buffer to minimum | **To do** |
| UniFi DHCP reservation for `owl` | To do |
| Strata + Qwen3.8-Flash-Next | To do |
| libosmos + DeepSeek-V4.1-Flash | To do |

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

## Scripts

- [`scripts/setup-rocm.sh`](scripts/setup-rocm.sh) installs ROCm and sets the GPU memory limit.
  Run it on `owl` as `jwmoss`.
