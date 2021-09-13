#include <stdio.h>

#include "freertos/FreeRTOS.h"
#include "freertos/portmacro.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "sdkconfig.h"

#define BLINK_GPIO  2
#define BLINK_DELAY 100 

static void led_task(void *pvParameter){
    while (1) {
        gpio_set_level(BLINK_GPIO, 0);
        vTaskDelay(BLINK_DELAY / portTICK_PERIOD_MS);

        gpio_set_level(BLINK_GPIO, 1);
        vTaskDelay(BLINK_DELAY / portTICK_PERIOD_MS);
    }
}

void app_main(void){
    gpio_reset_pin(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);

    xTaskCreate(&led_task, "led_task", 512, NULL, 5, NULL);

    printf("System Initiated\n");
    while(1){
        vTaskDelay(BLINK_DELAY / portTICK_PERIOD_MS);
    }
}
