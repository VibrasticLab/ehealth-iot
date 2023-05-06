#!/bin/bash

# adjust using ALSA-Mixer
# find device: 'arecord -L'

if [ -z "${1}" ]
then
    MICVOL=100%
else
    MICVOL=${1}%
fi

sudo rm -vf /var/lib/alsa/asound.state
amixer -D sysdefault:CARD=sndrpii2scard set I2SMic $MICVOL
sudo alsactl store
sudo alsactl nrestore

echo "You may need restart any program that access ALSA infrastructure"

