# Setup From Beginning

## Install Basic Packages

Guide Notes:
- https://github.com/mekatronik-achmadi/archmate/blob/master/notes/embedded/raspberry/guides/config_base.md
- https://github.com/mekatronik-achmadi/archmate/blob/master/notes/embedded/raspberry/guides/archmate/pkg_basic.txt

## Configure Display

Waveshare35 Guide Notes:
- https://github.com/mekatronik-achmadi/archmate/blob/master/notes/embedded/raspberry/guides/config_display.md

**WARNING:** Check if display Hi-Speed or not and adjust the driver settings in RaspberryPi's config.txt

**WARNING:** Check if display rotation settings in RaspberryPi's config.txt

## Try to Run

Just try run RaspberryPi using Waveshare35 display, then connect wifi using guide notes:
- https://github.com/mekatronik-achmadi/archmate/blob/master/notes/embedded/raspberry/guides/config_base.md

Then connect ssh/sshfs using command like:

```sh
ssh -Y alarm@10.124.4.230
sshfs alarm@10.124.4.230:/home/alarm sshmnt/
```

**TIPS:** You can use SSHFS for next steps

## Install Additional Infrastructures

### I2S MEMS driver
- https://aur.archlinux.org/packages/python-pyalsaaudio/ (Remove all Python2 setup)
- https://github.com/mekatronik-achmadi/archmate/tree/master/notes/embedded/raspberry/drivers/i2smems
- https://github.com/mekatronik-achmadi/archmate/blob/master/notes/embedded/raspberry/guides/config_audio.md

Reboot the unit

## Install Main Program

### GPIO Setup

Copy **pysources/gpio_config.sh**,  **pysources/mic_set.sh**, and **pysources/record_start.sh** to **/home/alarm/**.
Then test the program script using command:

```sh
bash /home/alarm/mic_set.sh 100
bash /home/alarm/gpio_config.sh
```

### Python GUI

Copy **pysources/coughgui/coughgui_demo_gpio.py** to **/home/alarm/**.
Then test the program using keyboard and Waveshare LCD Display with command:

```sh
startx /usr/bin/python /home/alarm/coughgui_demo_gpio.py &> testgui.txt
```

### Run At Start-Up

If everything works as expected, setup startup run by editing command:

```sh
sed -i 's@true@#true@g' ~/.bash_profile
sed -i 's@#exec startx@bash ~/gpio_config.sh;startx /usr/bin/python ~/coughgui_demo_gpio.py@g' ~/.bash_profile
```

## Backup the Image

You should backup the image content using note guides:
- https://github.com/mekatronik-achmadi/archmate/blob/master/notes/embedded/raspberry/guides/virtual_disk.md

