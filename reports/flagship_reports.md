# Flagship Reports

## Contents
- [Older Reports](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/flagship_reports.md#older-reports)
- [Augusts 2021](https://github.com/VibrasticLab/ehealth-iot/blob/master/reports/flagship_reports.md#august-2021)

## Older Reports

Older what already done can be see [here](https://github.com/mekatronik-achmadi/md_tutorial/blob/master/internship/task_0/done.md).

Older what planned can be see [here](https://github.com/mekatronik-achmadi/md_tutorial/blob/master/internship/task_0/planned.md).

## August 2021

Already built first basic prototype

![images](images/proto0.png?raw=true)

For I2S Mic Driver, here some step to setup:
- install I2S Mic kernel module from [here](- https://github.com/mekatronik-achmadi/archmate/tree/master/embedded/raspberrypi/drivers/i2smems/). **Notes:** It works with ALSA but not Pulseaudio
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