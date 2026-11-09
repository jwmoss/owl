# 3. ROCm and GPU memory

## ROCm

AMD's apt repository stops at ROCm 7.2.4 and has no Ubuntu 26.04 (`resolute`) packages.
`owl` uses the AMD TheRock build for `gfx1151` instead. The Strata Strix Halo guide uses the same build.

| Item | Value |
|------|-------|
| Archive | `https://repo.amd.com/rocm/tarball-multi-arch/therock-dist-linux-gfx1151-7.14.1.tar.gz` |
| SHA-256 | `c40e8f2bd6630a7d11557c762b99c6fa8afb04c9bd0e51ed1675ee1ca24afb00` |
| Install path | `/opt/rocm-7.14.1`, symlink `/opt/rocm` |
| HIP version | 7.14.60850 |
| Environment | `/etc/profile.d/rocm.sh` |
| Library path | `/etc/ld.so.conf.d/rocm.conf` |

libosmos expects `hipcc` and `rocminfo` in `/opt/rocm/bin`. The symlink gives that path.

`jwmoss` is in the `render` and `video` groups, so it can open `/dev/kfd` and `/dev/dri`.

Check the GPU:

```sh
rocminfo | grep -E "Marketing Name|Name: +gfx"
```

Expected: `AMD RYZEN AI MAX+ 395 w/ Radeon 8060S` and `gfx1151`.

## Memory split

The CPU and the GPU share 128 GB. Two settings control how the GPU uses it.

### 1. BIOS: UMA frame buffer (to do)

The BIOS gave a fixed 64 GB to the GPU. Linux then saw only 61 GB.
The engines use the GPU through GTT memory, which comes from the memory that Linux sees.
So set the fixed block to the minimum:

1. Reboot and press **Del**.
2. Find **UMA Frame Buffer Size** (or **iGPU Memory**), usually under
   **Advanced → AMD CBS → NBIO → GFX Configuration**.
3. Set it to the lowest value (512 MB or 1 GB).
4. Press **F10** to save.

Check after the reboot:

```sh
free -g                                                    # about 125 GB total
cat /sys/class/drm/card*/device/mem_info_vram_total        # small value
```

### 2. Kernel: ttm page limit

`/etc/modprobe.d/ttm.conf`:

```text
options ttm pages_limit=29637703 page_pool_size=29637703
```

This lets the GPU map about 113 GiB (29637703 pages of 4 KiB). libosmos checks for this value.
The initramfs was rebuilt, so the setting is active after the next reboot.

Check after the reboot:

```sh
cat /sys/module/ttm/parameters/pages_limit                 # 29637703
```
