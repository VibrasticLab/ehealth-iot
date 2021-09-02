# RaspberryPi Setup Summary

## Contents
- [Pre-Requisites](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#pre-requisites)
- [MMC Prepare](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#mmc-prepare)
- [Image Download](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#download-archlinuxarm-images)
	+ [RaspberryPi-4](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#raspberrypi-4)
	+ [RaspberryPi-3](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#raspberrypi-3)
- [Chroot Into MMC](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#chroot-into-mmc)
- [Upgrade Packages](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#upgrades-installed-package)
	+ [Initialize Pacman-Key](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#initialize-pacman-key)
	+ [Download Databases](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#download-database)
	+ [New Packages URLs](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#generate-new-packages-urls)
	+ [Download New Packages](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#download-new-packages)
	+ [Install New Packages](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#install-new-packages)
- [Required Package](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#required-packages)
	+ [Package List](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#package-list)
	+ [Required Packages URLs](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#required-packages-urls)
	+ [Download Required Packages](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#download-required-packages)
	+ [Install Required Packages](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#install-required-packages)
- [Global Configurations]()

## Pre-Requisites

These instructions done in ArchLinux in my laptops (except otherwise stated).

You can also use Manjaro or even Ubuntu/LinuxMint, but not Windows.

## MMC Prepare

Insert MMC into laptop either using built-in MMC reader or USB MMC Adapter.

**Notes:** Make sure that DEVDISK points to MMC you will use for RaspberryPi.
These instructions will format anything what DEVDISK points to.

```sh
sudo fdisk -l
export DEVDISK='/dev/sdb'

sudo parted ${DEVDISK} mklabel msdos

yes | sudo parted ${DEVDISK} mkpart primary 0% 200
yes | sudo parted ${DEVDISK} mkpart primary 200 100%
yes | sudo parted ${DEVDISK} set 1 lba on
yes | sudo parted ${DEVDISK} set 1 boot on

yes | sudo mkfs.vfat ${DEVDISK}1
yes | sudo mkfs.ext4 ${DEVDISK}2
```

## Download ArchLinuxARM Images

### RaspberryPi 4

```sh
wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-4-latest.tar.gz
```

### RaspberryPi 3

```sh
wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-2-latest.tar.gz
```

## Deploy Image

**Notes:** Make sure that DEVDISK points to MMC you will use for RaspberryPi.
These instructions will write to what DEVDISK points to.

```sh
sudo fdisk -l
export DEVDISK='/dev/sdb'

sudo mkdir -p /mnt/{boot,root}
sudo mount ${DEVDISK}1 /mnt/boot
sudo mount ${DEVDISK}2 /mnt/root

mkdir -p armv7h/
cd armv7h/

sudo bsdtar -xpf ../ArchLinuxARM-rpi-4-latest.tar.gz -C /mnt/root
sudo sync

sudo mv -vf /mnt/root/boot/* /mnt/boot/
sudo sync

sudo umount /mnt/root /mnt/boot
```

## Chroot Into MMC

Chrooting is process to mount other filesystem and change root shell into it.

First install Qemu ARM Static from this [AUR Package](https://aur.archlinux.org/packages/qemu-user-static-bin/)

Copy the binary into mounted MMC

```sh
sudo cp -vf /usr/bin/qemu-arm-static /mnt/root/usr/bin/
```

Then Chroot into it

```sh
sudo arch-chroot /mnt/root /bin/bash
```

---

## Upgrades Installed Package 

#### Initialize Pacman Key

```sh
pacman-key --init
pacman-key --populate archlinuxarm
```

---

#### Download Database

**Notes:** These instructions done in new shell outside the chrooted shell but in same working directory

```sh
mkdir -p databases/;cd databases/
echo "
http://mirror.archlinuxarm.org/armv6h/core/core.db
http://mirror.archlinuxarm.org/armv6h/core/core.files
http://mirror.archlinuxarm.org/armv6h/extra/extra.db
http://mirror.archlinuxarm.org/armv6h/extra/extra.files
http://mirror.archlinuxarm.org/armv6h/community/community.db
http://mirror.archlinuxarm.org/armv6h/community/community.files
http://mirror.archlinuxarm.org/armv6h/alarm/alarm.db
http://mirror.archlinuxarm.org/armv6h/alarm/alarm.files
http://mirror.archlinuxarm.org/armv6h/aur/aur.db
http://mirror.archlinuxarm.org/armv6h/aur/aur.files
" > ../dbase.txt
wget -i ../dbase.txt
cd ../
```

copy downloaded database files

```sh
sudo rsync -avh databases/ /mnt/root/var/lib/pacman/sync/
```

---

#### Generate New Packages URLs

```sh
pacman -Sup > /home/alarm/upgrade_pkgs.txt
```

---

#### Download New Packages

**Notes:** These instructions done in new shell outside the chrooted shell but in same working directory

```sh
cp -vf /mnt/root/home/alarm/upgrade_pkgs.txt ./
mkdir -p packages/official/;cd packages/official/
wget -i ../../upgrade_pkgs.txt
cd ../../
```

copy downloaded new package files

```sh
sudo rsync -avh packages/official/ /mnt/root/var/cache/pacman/pkg/
```

---

#### Install New Packages

```sh
sed -i "s#= Required DatabaseOptional#= Never#g" /etc/pacman.conf
sed -i "s#= Optional TrustAll#= Never#g" /etc/pacman.conf
sed -i "s#= Optional#= Never#g" /etc/pacman.conf

pacman -Su --noconfirm
```

---

## Required Packages

#### Package List

First download package list [here](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/pkg_basic.txt)

Then copy it to MMC using this command:

**Notes:** These instructions done in new shell outside the chrooted shell but in same working directory

```sh
cp -vf ../pkg_*.txt /mnt/root/home/alarm/pkglist.txt
```

---

#### Required Packages URLs

Now you can generate required packages urls

```sh
pacman -Sp $(cat /home/alarm/pkglist.txt) > /home/alarm/install_pkgs.txt
```

---

#### Download Required Packages

**Notes:** These instructions done in new shell outside the chrooted shell but in same working directory

```sh
cp -vf /mnt/root/home/alarm/install_pkgs.txt ./
mkdir -p packages/official/;cd packages/official/
wget -i ../../install_pkgs.txt
cd ../../
```

copy downloaded required package files 

```sh
sudo rsync -avh packages/official/ /mnt/root/var/cache/pacman/pkg/
```

---

#### Install Required Packages

```sh
sed -i "s#= Required DatabaseOptional#= Never#g" /etc/pacman.conf
sed -i "s#= Optional TrustAll#= Never#g" /etc/pacman.conf
sed -i "s#= Optional#= Never#g" /etc/pacman.conf

pacman -S --noconfirm $(cat /home/alarm/pkglist.txt)
```

---

## Global Configurations

#### Set Hostname (Optional)

```sh
echo "alarmrpi" > /etc/hostname
```

#### Silent Kernel/Systemd message (Optional)

```sh
sed -i '$s/$/ audit=0 quiet loglevel=0/' /boot/cmdline.txt
echo 'kernel.printk = 3 3 3 3' > /etc/sysctl.d/20-quiet-printk.conf
```

#### Generate new English locale

```sh
echo "LANG=en_US.UTF-8" > /etc/locale.conf
echo "en_US ISO-8859-1" >> /etc/locale.gen
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
```

#### Disable sudo passwords

```sh
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
passwd -d root
passwd -d alarm
```

#### Set Console Font

```sh
echo "FONT=ter-112n
FONT_MAP=8859-2
" > /etc/vconsole.conf
```

#### Enable Network Manager

```sh
systemctl disable dhcpd4
systemctl disable wpa_supplicant
systemctl disable systemd-networkd
systemctl enable NetworkManager
```

#### Enable SSH Server (Optional)

 ```sh
mkdir -p /etc/ssh
echo "
PermitRootLogin yes
AuthorizedKeysFile .ssh/authorized_keys
PermitEmptyPasswords yes
ChallengeResponseAuthentication no
UsePAM yes
PrintMotd no
Subsystem sftp /usr/lib/ssh/sftp-server
X11Forwarding yes
X11UseLocalhost yes
X11DisplayOffset 10
AllowTcpForwarding yes
" > /etc/ssh/sshd_config

systemctl enable sshd.service
```

#### Shell Autologin

```sh
mkdir -p /etc/systemd/system/getty@tty1.service.d/

echo "[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin alarm --noclear %I 38400 linux
" > /etc/systemd/system/getty@tty1.service.d/autologin.conf
```

---