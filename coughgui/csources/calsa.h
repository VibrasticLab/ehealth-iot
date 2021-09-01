/**
 * @file    calsa.h
 * @brief   C ALSA header.
 *
 * @addtogroup ALSA
 * @{
 */

#ifndef _CALSA_H_
#define _CALSA_H_

#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>

/**
 * @brief ALSA status OK
 */
#define ALSAOK  0

/**
 * @brief ALSA status Error
 */
#define ALSAERR 1

/**
 * @brief PCM NORMAL macro
 */
#define PCM_NORMAL 0

/**
 * @brief PCM frame buffer size
 */
#define BUFFERFRAME 512

/**
 * @brief PCM sample rate
 */
#define SAMPLERATE  44100

/**
 * @brief PCM channel size
 */
#define CHANNELSIZE  2

/**
 * @brief PCM width format
 */
#define PCMFORMAT SND_PCM_FORMAT_S16_LE

/**
 * @brief Maximum PCM range to normalize
 */
#define PCMSCALE 32768

/**
 * @brief ALSA Initialization
 * @details Initialize ALSA infrastructure
 */
int calsaInit(char *devName);

/**
 * @brief ALSA Capture
 * @details ALSA Capture function
 */
int calsaInput(short *buffer);

/**
 * @brief Close Function
 * @details Free some pointer in the end of program
 */
void calsaClose(void);

#endif

/** @} */