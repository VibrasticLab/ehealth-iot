#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wave
import requests

rawrecfile = "out.raw"
wavrecfile = "out.wav"

def sendrecord():
    with open(rawrecfile,"rb") as in_raw:
        rawdata = in_raw.read()
        with wave.open(wavrecfile,"wb") as out_wav:
            out_wav.setparams((2, 2, 44100, 0, 'NONE', 'NONE'))
            out_wav.writeframesraw(rawdata)

    files = {'file_batuk': open(wavrecfile,"rb")}
    values = {'nama': 'pasien', 'gender': 'unknown', 'umur': 0}
    requests.post("http://10.124.5.198/api/device/sendData/303",files=files, data=values)
    #requests.post("http://103.147.32.57/api/device/sendData/303",files=files, data=values)

if __name__ == "__main__":
    sendrecord()

