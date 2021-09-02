#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## command to record
# python alsarec.py

## command to playback
# aplay -r 44100 -f S16_LE -c 2 out.raw

import time as tm
import alsaaudio as alsa

if __name__ == "__main__":

    # raspberry I2S Mic in ALSA SoftVol
    device = 'dmic_sv'

    file = open('out.raw', 'wb')

    rawinput = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL,channels=2, rate=44100, format=alsa.PCM_FORMAT_S16_LE,periodsize=512, device=device)

    loops = 1000000
    while loops > 0:
        loops -= 1
        long, data = rawinput.read()

        if long:
            file.write(data)
            tm.sleep(0.01)

