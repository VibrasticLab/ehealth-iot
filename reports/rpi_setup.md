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
- [Global Configurations](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#global-configurations)
- [Complete Install](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#complete-install)
- [Spesific Configurations](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#spesific-configurations)
	+ [WiFi Connect](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#wifi-connect)
	+ [SSH Login](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#ssh-login)
	+ [LCD Waveshare35](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#lcd-waveshare35)
	+ [I2S Microphone](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#i2s-microphone)
	+ [I2S Microphone](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/rpi_setup.md#faster-running)

## Pre-Requisites

These instructions done in ArchLinux in laptops (except otherwise stated).

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

### RaspberryPi 2/3/4

```sh
wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-armv7-latest.tar.gz
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

sudo bsdtar -xpf ../ArchLinuxARM-rpi-armv7-latest.tar.gz -C /mnt/root
sudo sync

sudo mv -vf /mnt/root/boot/* /mnt/boot/
sudo sync

sudo umount /mnt/root /mnt/boot
```

**Notes**: This *armv7h* folder will be the default working directory

## Chroot Into MMC

Chrooting is process to mount other filesystem and change root shell into it.

First install Qemu ARM Static from this [AUR Package](https://aur.archlinux.org/packages/qemu-user-static-bin/)

Mount the MMC

```sh
sudo fdisk -l
export DEVDISK='/dev/sdb'

sudo mount ${DEVDISK}2 /mnt/root
sudo mount ${DEVDISK}1 /mnt/root/boot
```

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

### Initialize Pacman Key

```sh
pacman-key --init
pacman-key --populate archlinuxarm
```

---

### Download Database

**Notes:** These instructions done in new shell outside the chrooted shell but in same working directory

```sh
mkdir -p databases/;cd databases/
echo "
http://mirror.archlinuxarm.org/armv7h/core/core.db
http://mirror.archlinuxarm.org/armv7h/core/core.files
http://mirror.archlinuxarm.org/armv7h/extra/extra.db
http://mirror.archlinuxarm.org/armv7h/extra/extra.files
http://mirror.archlinuxarm.org/armv7h/community/community.db
http://mirror.archlinuxarm.org/armv7h/community/community.files
http://mirror.archlinuxarm.org/armv7h/alarm/alarm.db
http://mirror.archlinuxarm.org/armv7h/alarm/alarm.files
http://mirror.archlinuxarm.org/armv7h/aur/aur.db
http://mirror.archlinuxarm.org/armv7h/aur/aur.files
" > ../dbase.txt
wget -i ../dbase.txt
cd ../
```

copy downloaded database files

```sh
sudo rsync -avh databases/ /mnt/root/var/lib/pacman/sync/
```

---

### Generate New Packages URLs

```sh
pacman -Sup > /home/alarm/upgrade_pkgs.txt
```

---

### Download New Packages

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

### Install New Packages

```sh
sed -i "s#= Required DatabaseOptional#= Never#g" /etc/pacman.conf
sed -i "s#= Optional TrustAll#= Never#g" /etc/pacman.conf
sed -i "s#= Optional#= Never#g" /etc/pacman.conf

pacman -Su --noconfirm
```

---

## Required Packages

### Package List

First download package list [here](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/pkg_basic.txt)

Then copy it to MMC using this command:

**Notes:** These instructions done in new shell outside the chrooted shell but in same working directory

```sh
cp -vf ../pkg_*.txt /mnt/root/home/alarm/pkglist.txt
```

---

### Required Packages URLs

Now you can generate required packages urls

```sh
pacman -Sp $(cat /home/alarm/pkglist.txt) > /home/alarm/install_pkgs.txt
```

---

### Download Required Packages

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

### Install Required Packages

```sh
sed -i "s#= Required DatabaseOptional#= Never#g" /etc/pacman.conf
sed -i "s#= Optional TrustAll#= Never#g" /etc/pacman.conf
sed -i "s#= Optional#= Never#g" /etc/pacman.conf

pacman -S --noconfirm $(cat /home/alarm/pkglist.txt)
```

---

## Global Configurations

### workaround no HDMI bug (Optional)

```sh
echo "
hdmi_force_hotplug=1" >> /boot/config.txt
```

### Set Hostname (Optional)

```sh
echo "alarmrpi" > /etc/hostname
```

### Silent Kernel/Systemd message (Optional)

```sh
echo '
boot_delay=0
disable_splash=1' >> /boot/config.txt

sed -i '$s/$/ audit=0 quiet loglevel=0/' /boot/cmdline.txt
echo 'kernel.printk = 3 3 3 3' > /etc/sysctl.d/20-quiet-printk.conf

# if not using bluetooth
echo 'dtoverlay=disable-bt' >> /boot/config.txt
```

### Generate new English locale

```sh
echo "LANG=en_US.UTF-8" > /etc/locale.conf
echo "en_US ISO-8859-1" >> /etc/locale.gen
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
```

### Disable sudo passwords

```sh
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
passwd -d root
passwd -d alarm
```

### Set Console Font

```sh
echo "FONT=ter-112n
FONT_MAP=8859-2
" > /etc/vconsole.conf
```

### Enable Network Manager

```sh
systemctl disable dhcpd4
systemctl disable wpa_supplicant
systemctl disable systemd-networkd
systemctl enable NetworkManager
```

### Enable SSH Server

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

### Xorg Configuration

##### check vc4-kms-v3d driver

```sh
cat /boot/config.txt | grep vc4
```

##### dedicated gpu memory size

```sh
echo "gpu_mem=128" >> /boot/config.txt
```

##### fbdev config file

```sh
echo 'Section "Device"
	Identifier	"FBDEV"
	Driver		"fbdev"
	Option		"fbdev" "/dev/fb0"
	Option		"SwapbufferWait" "true"
EndSection' > /etc/X11/xorg.conf.d/99-fbdev.conf
```

### Shell Autologin

```sh
mkdir -p /etc/systemd/system/getty@tty1.service.d/

echo "[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin alarm --noclear %I 38400 linux
" > /etc/systemd/system/getty@tty1.service.d/autologin.conf
```

---

## Complete Install

Run this command to cleanup MMC and exiting after installation complete

```sh
rm -vf /home/alarm/{install_pkgs.txt,pkglist.txt,upgrade_pkgs.txt}
rm -vf /var/cache/pacman/pkg/*

exit
```

then unmount MMC

```sh
sudo umount /mnt/root/boot/
sudo umount /mnt/root/
```

Now you can boot MMC into actual RaspberryPi 2/3/4 unit

## Spesific Configurations

### Wifi Connect

For this section, you need to connect RaspberryPi display into regular HDMI or VGA display.

Also you need keyboard connected into one RaspberryPi USB 2.0

First enable RaspberryPi WiFi Radio:

```sh
sudo nmcli radio wifi on
```

Scan nearby WiFi:

```sh
sudo nmcli dev wifi
```


Now to connecting an WiFi, with known SSID and password:

```sh
sudo nmcli dev wifi connect CobaMQTT password "cobamqtt"
```

**Alternatively**, if you fancy NCurses interface, you can use:

```sh
sudo nmtui
```

Finally, after connected, check connected ip using:

```sh
ifconfig
```

### SSH Login

After RaspberryPi connected to a WiFi, you can now login into Raspberry via SSH without using connected Keyboard or Display

First you may want to remove known SSH server in your laptop:

```sh
rm -r ~/.ssh/
```

To login using RaspberryPi IP, use command:

```sh
ssh alarm@10.124.X.YYY
```

or if you need X11 forwarding:

```sh
ssh -Y alarm@10.124.X.YYY
```

From SSH you can do all things same as your local shell (vim, cp, mkdir, etc)

**Tips:** You can put this logic in RaspberryPi *~/.bashrc* to differentiate between normal login and SSH login

```
if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ]; then
    echo "SSH Login"
else
    echo "Normal Login"
fi
```


**Tips:** You can use SSHFS to mount a directory in RaspberryPi into you local directory.
Install [sshfs](https://archlinux.org/packages/community/x86_64/sshfs/) then you can mount using command

```sh
mkdir -p sshmnt/
sshfs alarm@192.168.X.YYY:/home/alarm sshmnt/
```

---

**CAUTION**: After this section, all next instructions are done in SSH/SSHFS into actual running RaspberryPi or using connected keyboard-display.
**NOT** chrooted in local shell.

### Bugfixes

##### DKMS Build Directory

In case you need some DKMS drivers, softlink "arm" build directory as "armv7l" so DKMS build can find it.

```sh
cd /usr/lib/modules/$(uname -r)/build/arch/
sudo ln -svf arm armv7l
cd ~
```

##### LibBLAS

In case BLAS implementation undetected by NumPy

```sh
sudo ln -svf libopenblas_armv7p-r0.3.19.so /usr/lib/libblas.so.3
```

### LCD Waveshare35

Download the overlay file waveshare35a.dts from [here](https://raw.githubusercontent.com/swkim01/waveshare-dtoverlays/master/waveshare35a.dts),
then copy it into home folder in actual RaspberryPi

```sh
dtc -@ -Hepapr -I dts -O dtb -o waveshare35a.dtbo waveshare35a.dts
sudo cp -f /home/alarm/waveshare35a.dtbo /boot/overlays/

sudo groupadd -fr video
sudo gpasswd -a alarm video
sudo gpasswd -a alarm tty

sudo sed -i '$s/$/ fbcon=font:ProFont6x11/' /boot/cmdline.txt
```

Next run this command to add these configuration into config.txt

For Waveshare35 (A):

```sh
echo "
dtparam=spi=on
dtoverlay=waveshare35a:rotate=270,swapxy=1" | sudo tee -a /boot/config.txt
```

For Waveshare35 (C) that using High SPI:

```sh
echo "
dtparam=spi=on
dtoverlay=waveshare35a:rotate=270,swapxy=1,speed=80000000" | sudo tee -a /boot/config.txt
```

**Notes:** If need to use potrait orientation, use **rotation=0** or **rotation=180**

And for touchscreen calibration, run this (**only** for rotation=270):

```sh
echo 'Section "InputClass"
    Identifier          "libinput touchscreen"
    MatchIsTouchScreen  "on"
    MatchDevicePath     "/dev/input/event*"
    Driver              "libinput"
    Option "TransformationMatrix" "1 0 0 0 -1 1 0 0 1"
EndSection'  | sudo tee /etc/X11/xorg.conf.d/99-calibration.conf
```

Lastly, to prevent Xorg blank sleeping, run this command:

```sh
echo 'Section "ServerFlags"
    Option "StandbyTime" "0"
    Option "SuspendTime" "0"
    Option "OffTime" "0"
    Option "BlankTime" "0"
EndSection'  | sudo tee /etc/X11/xorg.conf.d/noblank.conf
```

**Optionally**, if you also use HDMI along with, run this command:

```sh
sudo sed -i "s#/dev/fb0#/dev/fb1#g" /etc/X11/xorg.conf.d/99-fbdev.conf
```

**Reboot** using command

```sh
sudo reboot
```

then you can run gui programs using command like:

```sh
startx gtkprogram
```

or gui scripting:

```sh
startx /usr/bin/python3 gtkpython
```

### I2S Microphone

These instructions specificly using INMP441 I2S Microphone.

First install **I2S Microphone kernel module** from [here](https://github.com/mekatronik-achmadi/archmate/tree/master/embedded/raspberrypi/drivers/i2smems/)

Next run this command to add these configuration into config.txt

```sh
echo "
dtparam=audio=on
dtparam=i2s=on" | sudo tee -a /boot/config.txt
```

**Reboot** using command

```sh
sudo reboot
```

After reboot, you can check if I2S Mic register status using command:

```sh
arecord -l
```

it should be registered as *plughw:1*

Now, to boost volume, run this command to create file *~/.asoundrc*

```sh
echo "
pcm.dmic_hw {
	type hw
	card sndrpii2scard
	channels 2
	format S16_LE
}
pcm.dmic_sv {
	type softvol
	slave.pcm dmic_hw
	control {
		name I2SMic
		card sndrpii2scard
	}
	min_dB -3.0
	max_dB 30.0
}
" | tee $HOME/.asoundrc
```

Then run this command once for short period time (CTRL+Z to stop):

```sh
arecord -D dmic_sv -c2 -r 44100 -f S16_LE -t wav -V mono -v record.wav
```

After that, adjust the volume into 100% and store it as ALSA state

```sh
sudo rm -f /var/lib/alsa/asound.state
amixer -D sysdefault:CARD=sndrpii2scard set I2SMic 100%
sudo alsactl store
```

Now, to test a record (CTRL+Z to stop):

```sh
arecord -D dmic_sv -c2 -r 44100 -f S16_LE -t wav -V mono -v record.wav
```

for playback:

```sh
arecord -D dmic_sv -c2 -r 44100 -f S16_LE -t wav -V mono -v record.wav
```

for raw PCM playback:

```sh
aplay -r 44100 -f S16_LE -c 2 out.raw
```

**Tips:** If need Python wrapper for ALSA, you can install this [AUR Package](https://aur.archlinux.org/packages/python-pyalsaaudio/) (need Python3 only)

**Tips:** To maximize mic input, run **alsamixer** then press F6, select **snd_rpi_i2s_card**, then set to the max.

### Python Speech/Audio Analyzer (RPi-4)

##### install Librosa packages:

First create URL packages

```sh
export LIBROSAPKG="
python-joblib
python-decorator
python-scikit-learn
"

pacman -Sp $LIBROSAPKG > /home/alarm/librosa_pkg.txt
```

Then download packages in x86_64 laptop and copy them to mounted MMC

```sh
cp -vf ../sshmnt/librosa_pkg.txt ./
mkdir -p packages/official/;cd packages/official/
wget -i ../../librosa_pkg.txt
cd ../../

sudo rsync -avh package/official/ /mnt/root/var/cache/pacman/pkg/
```

Next install them

```sh
sudo pacman -S --noconfirm $(echo $LIBROSAPKG)
```

Last, install Librosa using PIP since their binaries are not available in ALARM and AUR repositories.

```sh
export LIBROSAPIP="
librosa audioread
soundfile resampy
numba pooch llvmlite
"

pip3 install -v -v -v --user --no-deps $LIBROSAPIP
```