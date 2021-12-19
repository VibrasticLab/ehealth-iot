#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import alsaaudio as alsa

device = 'dmic_sv'
file = open('out.raw', 'wb')

rawinput = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL,channels=2, rate=44100, format=alsa.PCM_FORMAT_S16_LE,periodsize=512, device=device)
long, data = rawinput.read()
decoded = np.frombuffer(data, dtype='i2' )
print('Array PCM: \n',decoded)

file.write(data)
file.flush()
file.close()


