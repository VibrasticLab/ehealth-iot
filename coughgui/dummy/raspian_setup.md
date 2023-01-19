# Raspbian Setup for Dummy Unit

## Update and Upgrade

run commands:

```sh
sudo apt-get update
sudo apt-get upgrade
```

## Install SSH

Run this command:

```sh
sudo raspi-config
```

then choose following menu: *Interface Options -> SSH -> YES -> OK*

Now you can select *Finish* and then you can login from SSH using username and password like:

```sh
ssh username@ip-number
```

**NOTES:** Next commands here can be done in SSH

## Additional Packages

```sh
sudo apt-get install git tig vim mc tmux fonts-terminus libncurses-dev
```

## Build TTYPlot

```sh
git clone https://github.com/tenox7/ttyplot.git
cd ttyplot/
make -j$(nproc)
sudo cp -vf ./ttyplot /usr/bin/
```

## Display Configs

```sh
wget -c https://raw.githubusercontent.com/swkim01/waveshare-dtoverlays/master/waveshare35a.dts
dtc -@ -Hepapr -I dts -O dtb -o waveshare35a.dtbo waveshare35a.dts
sudo cp -vf waveshare35a.dtbo /boot/overlays/

echo "
dtparam=spi=on
dtoverlay=waveshare35a:rotate=180,swapxy=1" | sudo tee -a /boot/config.txt

sudo sed -i '$s/$/ fbcon=font:ProFont6x11/' /boot/cmdline.txt
```

## Settings

```sh
echo '
boot_delay=0
disable_splash=1' | sudo tee -a /boot/config.txt

sudo sed -i '$s/$/ audit=0 quiet loglevel=0/' /boot/cmdline.txt
echo 'kernel.printk = 3 3 3 3' | sudo tee /etc/sysctl.d/20-quiet-printk.conf

echo 'PermitEmptyPasswords yes' | sudo tee -a /etc/ssh/sshd_config

sudo mkdir -p /etc/systemd/system/getty@tty1.service.d/

echo "[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin $USER --noissue --noclear %I 38400 linux
" | sudo tee /etc/systemd/system/getty@tty1.service.d/autologin.conf

echo "[Service]
TTYVTDisallocate=no
" | sudo tee /etc/systemd/system/getty@tty1.service.d/noclear.conf

echo "FONT=ter-112n
FONT_MAP=8859-2
" | sudo tee /etc/vconsole.conf

sudo passwd -d $USER
```

## Dummy Program

```sh
mkdir -p ~/dummy/;cd ~/dummy/
wget -c https://raw.githubusercontent.com/VibrasticLab/ehealth-iot/master/coughgui/dummy/randomplot/main.sh
wget -c https://raw.githubusercontent.com/VibrasticLab/ehealth-iot/master/coughgui/dummy/randomplot/randomplot.sh

echo '
[[ -f ~/.bashrc ]] && . ~/.bashrc
source ~/.bashrc

if [ -n "$SSH_CLIENT" ] || [ -n "$SSH_TTY" ]; then
    echo "SSH Login Success"
else
    if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
        #true
        ~/dummy/main.sh
    fi
fi' | tee $HOME/.bash_profile
```

