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
sudo apt-get install git tig vim mc tmux libncurses-dev
```

## Build TTYPlot

```sh
git clone https://github.com/tenox7/ttyplot.git
cd ttyplot/
make
sudo cp -vf ./ttyplot /usr/bin/
```