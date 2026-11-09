# 2. Ubuntu install

## Why Ubuntu Server 26.04 LTS

- The AMD ROCm compatibility matrix lists Ubuntu 26.04.1 (GA kernel 7.0) and `gfx1151`.
- The Server edition imports SSH keys from GitHub during the install.
- No desktop runs, so the models get more memory.

## Install

1. Boot from the network (see [01-netboot.md](01-netboot.md)).
2. Select **Linux Network Installs → Ubuntu → 26.04 LTS → Ubuntu Server**.
3. Storage: use the entire disk. Turn off LVM, or set `ubuntu-lv` to the full size.
   The default LVM layout makes a root volume of only about 100 GB. The models need more than 400 GB.
4. Profile: server name `owl`, user `jwmoss`.
5. Ubuntu Pro: skip.
6. SSH: install OpenSSH server, import keys **from GitHub**, user `jwmoss`. Turn off password login over SSH.
7. Featured snaps: skip.
8. Reboot. Remove the network cable or press **F7** and pick the NVMe disk, so the machine does not PXE boot again.

## Passwordless sudo

Run this one time from a real terminal (it asks for the password):

```sh
ssh -t jwmoss@192.168.1.241 'echo "jwmoss ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/90-jwmoss && sudo chmod 440 /etc/sudoers.d/90-jwmoss'
```

Only the SSH key can log in, so this is safe on the home network.
