# 1. Ubuntu install

## Why Ubuntu Server 26.04 LTS

- The AMD ROCm compatibility matrix lists Ubuntu 26.04 (GA kernel 7.0) and `gfx1151`.
- The Server edition imports SSH keys from GitHub during the install.
- No desktop runs, so the models get more memory.

## BIOS

Press **Del** at power on (GMKtec EVO-X2; other machines can use a different key).

1. Set **UMA Frame Buffer Size** (or **iGPU Memory**) to the minimum.
   It is usually under **Advanced → AMD CBS → NBIO → GFX Configuration**. The EVO-X2 minimum is 2 GB.
2. Set **Secure Boot** to Disabled.
3. Press **F10** to save.

The engines use the GPU through GTT memory, which comes from the memory that Linux sees.
A large fixed frame buffer (the default is often 64 GB) hides that memory from Linux.

## Boot the installer

Use a USB stick with the [Ubuntu Server 26.04 image](https://ubuntu.com/download/server), or boot from the network.

To boot from the network with [netboot.xyz](https://netboot.xyz):

- Enable **Network Stack** and **IPv4 PXE Support** in the BIOS. On the EVO-X2, press **F7** at power on
  and select **UEFI: PXE IPv4**.
- Set the DHCP boot file to `netboot.xyz-snponly.efi`, not `netboot.xyz.efi`. The full build loads its own
  USB drivers, and on the EVO-X2 those drivers stop the USB keyboard.
- If iPXE shows error `0216eb8f` ("no usable certificates"), update the netboot.xyz menus. Old menus have
  an old certificate store.
- In netboot.xyz, select **Linux Network Installs → Ubuntu → 26.04 LTS → Ubuntu Server**.

## Install

1. Storage: use the entire disk. Turn off LVM, or set `ubuntu-lv` to the full size.
   The default LVM layout makes a root volume of only about 100 GB. All engines together need about 900 GB.
2. Profile: set the server name and your user.
3. Ubuntu Pro: skip.
4. SSH: install OpenSSH server and import your keys from GitHub. Turn off password login over SSH.
5. Featured snaps: skip.
6. Reboot.

## Passwordless sudo

Ansible needs `sudo` without a password. Run this one time from a terminal (it asks for the password):

```sh
ssh -t <user>@<host> 'echo "<user> ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/90-<user> && sudo chmod 440 /etc/sudoers.d/90-<user>'
```

Do this only when SSH accepts keys and not passwords.
