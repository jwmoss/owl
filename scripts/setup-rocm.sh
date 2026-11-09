#!/usr/bin/env bash
# Install ROCm 7.14.1 (TheRock, gfx1151) and set the GPU memory limit on owl.
# Run as jwmoss with passwordless sudo. Reboot after it finishes.
set -euo pipefail

readonly ROCM_VERSION="7.14.1"
readonly ROCM_ARCHIVE="therock-dist-linux-gfx1151-${ROCM_VERSION}.tar.gz"
readonly ROCM_URL="https://repo.amd.com/rocm/tarball-multi-arch/${ROCM_ARCHIVE}"
readonly ROCM_SHA256="c40e8f2bd6630a7d11557c762b99c6fa8afb04c9bd0e51ed1675ee1ca24afb00"
readonly TTM_PAGES="29637703" # about 113 GiB of 4 KiB pages

sudo DEBIAN_FRONTEND=noninteractive apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
  build-essential cmake ninja-build git pipx python3-pip python3-venv \
  libnuma1 libelf1t64 libdrm-amdgpu1 nvtop btop

workdir="$(mktemp -d)"
trap 'rm -rf "${workdir}"' EXIT
curl -fsSL -o "${workdir}/${ROCM_ARCHIVE}" "${ROCM_URL}"
echo "${ROCM_SHA256}  ${workdir}/${ROCM_ARCHIVE}" | sha256sum -c -

sudo mkdir -p "/opt/rocm-${ROCM_VERSION}"
sudo tar -xzf "${workdir}/${ROCM_ARCHIVE}" -C "/opt/rocm-${ROCM_VERSION}"
sudo ln -sfn "/opt/rocm-${ROCM_VERSION}" /opt/rocm

sudo usermod -aG render,video "${USER}"

echo "options ttm pages_limit=${TTM_PAGES} page_pool_size=${TTM_PAGES}" |
  sudo tee /etc/modprobe.d/ttm.conf >/dev/null

sudo tee /etc/profile.d/rocm.sh >/dev/null <<'EOF'
export ROCM_PATH=/opt/rocm HIP_PATH=/opt/rocm HIP_PLATFORM=amd
export PATH=/opt/rocm/bin:/opt/rocm/lib/llvm/bin:$PATH
export LD_LIBRARY_PATH=/opt/rocm/lib:/opt/rocm/lib/rocm_sysdeps/lib:/opt/rocm/lib/llvm/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
EOF

printf '%s\n' /opt/rocm/lib /opt/rocm/lib/rocm_sysdeps/lib /opt/rocm/lib/llvm/lib |
  sudo tee /etc/ld.so.conf.d/rocm.conf >/dev/null
sudo ldconfig
sudo update-initramfs -u -k all

/opt/rocm/bin/rocminfo | grep -m2 -E "Name: +gfx|Marketing Name"
echo "Done. Reboot to apply the ttm limit and the new groups."
