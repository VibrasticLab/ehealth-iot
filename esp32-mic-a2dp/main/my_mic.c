/**
 * example in use: https://www.esp32.com/viewtopic.php?t=15185
 * cross-reference with: https://github.com/runnisha477/Audio-Input-PCMI2S/blob/main/audio_record.ino
 */

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_now.h"
#include "esp_console.h"
#include "driver/i2s.h"
#include "driver/uart.h"
#include "argtable3/argtable3.h"

#include "my_mic.h"
#include "myconfig.h"

uint8_t recStatus;

static void micRaw(uint16_t* buffRaw){
    int i, samplesRead;
    size_t bytesRead = 0;
    uint8_t buff32[ESP_NOW_MAX_DATA_LEN*4] = {0};

    i2s_read(I2S_NUM_0, &buff32, sizeof(buff32), &bytesRead, 100);
    samplesRead = bytesRead/4;

    for(i=0;i<samplesRead;i++){
        uint8_t mid = buff32[i*4+2];
        uint8_t msb = buff32[i+4+3];
        uint16_t raw = (((uint32_t)msb)<<8) + ((uint32_t)mid);
        memcpy(&buffRaw[i], &raw, sizeof(raw));
    }
}

static void micTask(void *pvParameter){
    uint16_t i;
    uint16_t rec16[ESP_NOW_MAX_DATA_LEN] = {0};
    recStatus = 0;

    while(1){
        if(recStatus==1){
            micRaw(rec16);
            for(i=0;i<ESP_NOW_MAX_DATA_LEN;i++){
                printf("%i ",rec16[i]);
            }
        }
        vTaskDelay(100 / portTICK_PERIOD_MS);
    }
}

static int get_raw(int argc, char **argv){
    if(recStatus==0){recStatus=1;}
    else{recStatus=0;}

    return 0;
}

static void micRegister(void){
    const esp_console_cmd_t cmd = {
        .command = "mic",
        .help = "Test Microphone",
        .hint = NULL,
        .func = &get_raw,
    };
    esp_console_cmd_register(&cmd);
}

void micInit(void){

    i2s_config_t micConf = {
        .mode = (i2s_mode_t) (I2S_MODE_MASTER|I2S_MODE_RX),
        .sample_rate = 44100,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = (i2s_comm_format_t) (I2S_COMM_FORMAT_STAND_I2S | I2S_COMM_FORMAT_STAND_MSB),
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
        .dma_buf_count = 4,
        .dma_buf_len = ESP_NOW_MAX_DATA_LEN * 4,
        .use_apll = false,
        .tx_desc_auto_clear = false,
        .fixed_mclk = 0,
    };

    if(i2s_driver_install(I2S_NUM_0, &micConf, 0, NULL) != ESP_OK){
        printf("I2S driver install error\r\n");
    }

    i2s_pin_config_t micPin = {
        .bck_io_num = 14,
        .ws_io_num = 15,
        .data_out_num = -1,
        .data_in_num = 13,
    };

    if(i2s_set_pin(I2S_NUM_0, &micPin) != ESP_OK){
        printf("I2S pin set error\r\n");
    }

    xTaskCreate(&micTask, "mic_task", 4096, NULL, 5, NULL);

    micRegister();
}
