# RaspberryPi Setup Summary

## Contents
- [Pre-Requisites]()
- [MMC Prepare]()
- [Image Download]()
	+ [RaspberryPi-4]()
	+ [RaspberryPi-3]()
- [Chroot Into MMC]()
- [Upgrade Packages]()
	+ [Initialize Pacman-Key]()
	+ [Download Databases]()
	+ [New Packages URLs]()
	+ [Download New Packages]()
	+ [Install New Packages]()

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

First install Qemu ARM Static from [AUR Package](https://aur.archlinux.org/packages/qemu-user-static-bin/)

Copy the binary into mounted MMC

```sh
sudo cp -vf /usr/bin/qemu-arm-static /mnt/root/usr/bin/
```

Then Chroot into it

```sh
sudo arch-chroot /mnt/root /bin/bash
```

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

#### Download New Packages

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

#### Install New Packages

```sh
sed -i "s#= Required DatabaseOptional#= Never#g" /etc/pacman.conf
sed -i "s#= Optional TrustAll#= Never#g" /etc/pacman.conf
sed -i "s#= Optional#= Never#g" /etc/pacman.conf

pacman -Su --noconfirm
```
