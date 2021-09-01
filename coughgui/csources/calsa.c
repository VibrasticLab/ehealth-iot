 /**
 * @file    calsa.c
 * @brief   C ALSA code.
 *
 * @addtogroup ALSA
 * @{
 */

#include "calsa.h"
#include <asm-generic/errno-base.h>
#include <stdlib.h>
 
 /* ALSA parameters */
snd_pcm_t *captureHandle;
snd_pcm_hw_params_t *hwParams;
unsigned int sampleRate = SAMPLERATE;

int calsaInit(char *devName){
    int err;

    if ((err=snd_pcm_open(&captureHandle,devName,SND_PCM_STREAM_CAPTURE,PCM_NORMAL))<0) {
        fprintf(stderr,"failed open %s device (%s)\n",devName,snd_strerror(err));
        return ALSAERR;
    }

    if((err=snd_pcm_hw_params_malloc(&hwParams))<0){
        fprintf(stderr,"failed allocate hwparams (%s)\n",snd_strerror(err));
        return ALSAERR;
    }

    if((err=snd_pcm_hw_params_any(captureHandle,hwParams))<0){
        fprintf(stderr,"failed initialize hwparams (%s)\n",snd_strerror(err));
        return ALSAERR;
    }

    if ((err=snd_pcm_hw_params_set_access(captureHandle,hwParams,SND_PCM_ACCESS_RW_INTERLEAVED))<0){
        fprintf(stderr,"failed set access type (%s)\n",snd_strerror(err));
        return ALSAERR;
    }

    if ((err=snd_pcm_hw_params_set_format(captureHandle,hwParams,PCMFORMAT))<0){
        fprintf(stderr,"failed set format type (%s)\n",snd_strerror(err));
        return ALSAERR;
    }

    if ((err=snd_pcm_hw_params_set_rate_near(captureHandle,hwParams,&sampleRate,0))<0){
        fprintf(stderr,"failed set sample rate (%s)\n",snd_strerror(err));
        return ALSAERR;
    }

    if ((err=snd_pcm_hw_params_set_channels (captureHandle,hwParams,CHANNELSIZE))<0){
        fprintf(stderr,"failed set channels (%s)\n",snd_strerror(err));
        return ALSAERR;
    }

    if ((err = snd_pcm_hw_params (captureHandle,hwParams))<0) {
        fprintf (stderr,"failed set hw params (%s)\n",snd_strerror(err));
        return ALSAERR;
    }

    if((err=snd_pcm_prepare(captureHandle))<0){
        fprintf (stderr,"failed prepare interface (%s)\n",snd_strerror(err));
        return ALSAERR;
    }

    return ALSAOK;
 }

int calsaInput(short *buffer){
    int err;
    err=snd_pcm_readi(captureHandle, buffer, BUFFERFRAME);
    
    /* overrun (broken pipe) error */
    if(err==-EPIPE){
        snd_pcm_prepare(captureHandle);
        return ALSAERR;
    }
    
    if(err!=-EPIPE){
        if(err==-EAGAIN){
            err = 0;
            return ALSAOK;
        }
        else if (err<0) {
            fprintf (stderr, "read audio failed (%s)\n",snd_strerror(err));
            return ALSAERR;
        }
    }

    return ALSAOK;
 }

void calsaClose(void){
    snd_pcm_hw_params_free(hwParams);
    snd_pcm_close(captureHandle);
}

 /** @} */