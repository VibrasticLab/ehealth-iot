/**
 * Minimal Audio Capture using ALSA
 *
 * Configuration: stereo, 16LE, 44100 Hz
 *
 * From on Paul David's tutorial : http://equalarea.com/paul/alsa-audio.html
 *
 * sudo pacman -S alsa-lib
 * gcc -o calsa -lasound calsa.c && ./calsa hw:0
 * gcc -o calsa -lasound calsa.c && ./calsa dmic_sv
 */

 /**
 * @file    calsa.c
 * @brief   ALSA Capture Test code.
 *
 * @addtogroup ALSA
 * @{
 */

#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>

/**
 * @brief Main function
 */
int main (int argc, char *argv[]){
    /* general variables */
    int i;
    int err;

    /* buffer parameters */
    char *buffer;
    int bufferFrame = 512;
    unsigned int rate = 44100;

    /* ALSA parameters */
    snd_pcm_t *captureHandle;
    snd_pcm_hw_params_t *hwParams;
    snd_pcm_format_t format = SND_PCM_FORMAT_S16_LE;

    /* try open input device */
    if ((err=snd_pcm_open(&captureHandle, argv[1] , SND_PCM_STREAM_CAPTURE, 0))<0) {
        fprintf(stderr, "failed open %s device (%s)\n", argv[1],snd_strerror(err));
        return 1;
    }

    return 0;
}

/** @} */
