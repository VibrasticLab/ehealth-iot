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

#define SHORT_TEST 0

/**
 * @brief Main function
 */
int main (int argc, char *argv[]){
    /* general variables */
    int err;
    unsigned int i;

#if SHORT_TEST
    unsigned int sz;
#endif

    /* buffer parameters */
    char *buffer;
    int bufferFrame = 128;
    unsigned int rate = 44100;
    unsigned char channels = 2;

    /* ALSA parameters */
    snd_pcm_t *captureHandle;
    snd_pcm_hw_params_t *hwParams;
    snd_pcm_format_t format = SND_PCM_FORMAT_S16_LE;

    /* raw file */
    FILE *rawfile;

    /* try open input device */
    if ((err=snd_pcm_open(&captureHandle,argv[1],SND_PCM_STREAM_CAPTURE,0))<0) {
        fprintf(stderr,"failed open %s device (%s)\n",argv[1],snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"device %s opened\n",argv[1]);

    /* hw params allocated */
    if((err=snd_pcm_hw_params_malloc(&hwParams))<0){
        fprintf(stderr,"failed allocate hwparams (%s)\n",snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"hw_params allocated\n");

    /* hw params initialized */
    if((err=snd_pcm_hw_params_any(captureHandle,hwParams))<0){
        fprintf(stderr,"failed initialize hwparams (%s)\n",snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"hw_params initialized\n");

    /* hw params set access*/
    if ((err=snd_pcm_hw_params_set_access(captureHandle,hwParams,SND_PCM_ACCESS_RW_INTERLEAVED))<0){
        fprintf(stderr,"failed set access type (%s)\n",snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"access type OK\n");

    /* hw params set format */
    if ((err=snd_pcm_hw_params_set_format(captureHandle,hwParams,format))<0){
        fprintf(stderr,"failed set format type (%s)\n",snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"format type OK\n");

    /* hw params set rate */
    if ((err=snd_pcm_hw_params_set_rate_near(captureHandle,hwParams,&rate,0))<0){
        fprintf(stderr,"failed set sample rate (%s)\n",snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"sample rate OK\n");

    /* hw params set channels*/
    if ((err=snd_pcm_hw_params_set_channels (captureHandle,hwParams,channels))<0){
        fprintf(stderr,"failed set channels (%s)\n",snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"channels OK\n");

    /* actual hw params set*/
    if ((err = snd_pcm_hw_params (captureHandle,hwParams))<0) {
        fprintf (stderr,"failed set hw params (%s)\n",snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"all hw_params OK\n");
    snd_pcm_hw_params_free(hwParams);

    /* prepare audio interface */
    if((err=snd_pcm_prepare(captureHandle))<0){
        fprintf (stderr,"failed prepare interface (%s)\n",snd_strerror(err));
        return 1;
    }
    fprintf(stdout,"audio interface prepared\n");

    /* allocate buffer */
    buffer = malloc(bufferFrame*snd_pcm_format_width(format)/8*channels);
    fprintf(stdout,"buffer allocated\n");

    /* open raw file */
    if((rawfile=fopen(argv[2],"ab"))==NULL){
        fprintf(stdout,"failed open raw file target\n");
        return 1;
    }
    fprintf(stdout,"opened raw target file\n");

    /* test read */
#if SHORT_TEST
    for(i=0;i<10;++i){
        if ((err=snd_pcm_readi(captureHandle, buffer, bufferFrame))!=bufferFrame) {
            fprintf (stderr,"read from audio interface failed (%s)\n",snd_strerror(err));
            return 1;
        }
        sz = sizeof(buffer);
        fprintf(stdout,"test read %d done in %d\n",i,sz);
    }
#else
    for(i=0;i<2000;++i){
        snd_pcm_readi(captureHandle,buffer,bufferFrame);
        fwrite(buffer,1,channels*bufferFrame,rawfile);
    }
#endif
    free(buffer);

    snd_pcm_close(captureHandle);   
    fprintf(stdout,"audio interface closed\n");

    return 0;
}

/** @} */
