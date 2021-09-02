# Flagship Reports

## Contents
- [Older Reports](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/flagship_reports.md#older-reports)
- [Augusts 2021](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/flagship_reports.md#august-2021)
- [September 2021]()

## Older Reports

Older what already done can be see [here](https://github.com/mekatronik-achmadi/md_tutorial/blob/master/internship/task_0/done.md).

Older what planned can be see [here](https://github.com/mekatronik-achmadi/md_tutorial/blob/master/internship/task_0/planned.md).

## August 2021

Already built first basic prototype

![images](images/proto0.png?raw=true)

---

For I2S Mic Driver, here some step to setup:
- install I2S Mic kernel module from [here](https://github.com/mekatronik-achmadi/archmate/tree/master/embedded/raspberrypi/drivers/i2smems/).

**Notes:** It works with ALSA but not Pulseaudio. Bugfixes needed

- Reboot
- write this ALSA config on *~/.asoundrc* file:

```
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
```

- run this command for short time once

```sh
arecord -D dmic_sv -c2 -r 44100 -f S16_LE -t wav -V mono -v record.wav
```

- Set I2S Mic at maximum volume

```sh
sudo rm -f /var/lib/alsa/asound.state
amixer -D sysdefault:CARD=sndrpii2scard set I2SMic 100%
sudo alsactl store
```

- Now I2S Mic ready to use via ALSA and it's wrapper

---

Python ALSA Wrapper

To access I2S Mic from ALSA using Python, you can install it's wrapper first.

For Arch-Linux ARM or its derivatives, you can install this [AUR Package](https://aur.archlinux.org/packages/python-pyalsaaudio/)

Then you can test using this Python3 script:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time as tm
import alsaaudio as alsa

if __name__ == "__main__":

    device = 'dmic_sv'

    file = open('out.raw', 'wb')

    rawinput = alsa.PCM(alsa.PCM_CAPTURE,alsa.PCM_NORMAL,channels=2,rate=44100,
    			format=alsa.PCM_FORMAT_S16_LE,periodsize=512, device=device)

    loops = 1000000
    while loops > 0:
        loops -= 1
        long, data = rawinput.read()

        if long:
            file.write(data)
            tm.sleep(0.01)
```

Press **CTRL+C** to stop, then you can replay record using command:

```sh
aplay -r 44100 -f S16_LE -c 2 out.raw
```

The Interface shown above made by combining Matplotlib Graph, Tkinter GUI, Python ALSA wrapper, and Python Numpy.

You can found the script prototype [here](https://github.com/VibrasticLab/ehealth-iot/blob/master/coughgui/pysources/coughgui.py)

---

Next plan to build a PCB Shield to replace jumper cables and make more compact design.

![images](images/shield_pcb.png?raw=true)

![images](images/shield_3d.png?raw=true)

PCB order planned from [Tokped](https://www.tokopedia.com/geraicerdas/cetak-pcb-1-keping-single-double-layer-rapid-prototyping-satuan)

Component need to buy is a Long Male-Female header from [Tokped](https://www.tokopedia.com/mulsanne/stack-stackable-header-1x40-male-female-untuk-arduino-shield)

---

## September 2021

### What's done:

Tested High Speed SPI LCD from [Tokped](https://www.tokopedia.com/digiware/lcd-3-5-inch-resistive-touch-screen-480x320-high-spi-raspberry-pi).

Still use *waveshare35a* overlay (since it init code compatibility),
but maximum SPI clock now up to 80MHz instead 20MHz like previous.

---

The code now available in two form, C and Python.
Despite different implementation languages, both using ALSA API wrapped in their own ways

### Python:

Python script [here](https://github.com/VibrasticLab/ehealth-iot/blob/master/coughgui/pysources/coughgui.py)

Using PyALSA (ALSA Python wrapper) [here](http://larsimmisch.github.io/pyalsaaudio/), Tkinter, Numpy, and Matplotlib libraries 

![images](images/sep2021_0.jpg?raw=true)

### C:

C source-tree [here](https://github.com/VibrasticLab/ehealth-iot/tree/master/coughgui/csources/cgtk)

Using ALSA API directly, GTK3, Cairo, and [Slope](https://github.com/bytebrew/slope) plotting libraries

There are still some problem for C implementation:
- Correct chunk array variable memory allocation
- Overrun and other capture error handling
- Latency between audio and graph
- write RAW/WAVE output test

![images](images/sep2021_1.jpg?raw=true)

---

### Waiting components

Next is get rid of those signal cables by replacing it with a PCB Shield ordered [here](https://www.tokopedia.com/geraicerdas/cetak-pcb-1-keping-single-double-layer-rapid-prototyping-satuan)

Now shipping:

![images](images/sep2021_2.jpg?raw=true)
 
 ---
 
### Planned Next:
 - Implement audio or cough analyzer in either C or Python Implementation
 - Build packaging after PCB Shield arrived and successfully tested
 
---

### Next Job:
- I2SMic input to ESP32


