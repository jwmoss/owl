# 1. Network boot with netboot.xyz

`owl` installs its OS over the network. The netboot.xyz container on the Unraid server gives the boot files.
The UniFi gateway tells PXE clients where to find them.

## netboot.xyz on Unraid

| Item | Value |
|------|-------|
| Host | Unraid `Tower`, `192.168.1.254` |
| Container | `netbootxyz`, image `ghcr.io/netbootxyz/netbootxyz` |
| Network | `br0`, own IP `192.168.1.248` |
| TFTP | UDP 69, root `/config/menus` |
| Web UI | `http://192.168.1.248:3000` |
| Assets | `http://192.168.1.248:80` |
| Config | `/mnt/user/appdata/netbootxyz` → `/config` |
| Assets folder | `/mnt/user/appdata/netbootxyz_images` → `/assets` |

### Menu version

The container image updates, but the menus in `/config/menus` do not. Old menus contain an old iPXE
certificate store. An old store causes iPXE error `0216eb8f` ("no usable certificates") when you pick an OS.

On 2026-11-08 the menus went from 2.0.87 to 3.0.3:

1. Back up `menus/` to `menus.bak-<timestamp>`.
2. Download `menus.tar.gz`, `autoexec.ipxe` and the `.efi` and `.kpxe` boot files from the
   [netboot.xyz release](https://github.com/netbootxyz/netboot.xyz/releases).
3. Check the boot files against `netboot.xyz-sha256-checksums.txt`.
4. Extract the files into `menus/` and set `menuversion.txt`.
5. Keep the owner `1000:1000` and restart the container.

You can also use **Menus → update** in the web UI.

## UniFi DHCP

Network **Default** (`192.168.1.0/24`) → DHCP → Network Boot:

| Setting | Value |
|---------|-------|
| Network boot | On |
| Boot server / TFTP server | `192.168.1.248` |
| Boot file | `netboot.xyz-snponly.efi` |

Use `netboot.xyz-snponly.efi`, not `netboot.xyz.efi`. The full build loads its own USB drivers.
On the EVO-X2 those drivers stop the USB keyboard. The `snponly` build uses only the firmware drivers.

The IoT and Guest networks do not have network boot.

Custom DHCP option 175 (`nginx`, text `http://192.168.1.248:80/`) is set on Default. netboot.xyz does not use it.
It does not stop the boot.

## Switch port

`owl` is on Office Switch port 8. That port had native network **Guest**, so the PXE boot failed.
On 2026-11-08 the native network changed to **Default**.

## Boot the EVO-X2 from the network

1. In the BIOS (**Del**), set **Network Stack** and **IPv4 PXE Support** to Enabled.
2. Set **Secure Boot** to Disabled.
3. At power on, press **F7** and select **UEFI: PXE IPv4**.
4. To see the boot on the server, run `docker logs -f netbootxyz` on `Tower`.

At the `iPXE>` prompt, type `reboot` to restart or `exit` to go back to the firmware.
