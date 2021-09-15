#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "sdkconfig.h"
#include "esp_system.h"
#include "esp_console.h"
#include "esp_log.h"
#include "esp_vfs_dev.h"
#include "esp_err.h"
#include "nvs_flash.h"
#include "driver/uart.h"
#include "linenoise/linenoise.h"
#include "argtable3/argtable3.h"

#include "my_cmd.h"
#include "my_wifista.h"
#include "myconfig.h"

static void ledTask(void *pvParameter){
    while (1) {
        gpio_set_level(BLINK_GPIO, 0);
        vTaskDelay(BLINK_DELAY / portTICK_PERIOD_MS);

        gpio_set_level(BLINK_GPIO, 1);
        vTaskDelay(BLINK_DELAY / portTICK_PERIOD_MS);
    }
}

static void nvsInit(void){
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}

static void consoleInit(void){
    fflush(stdout);
    fsync(fileno(stdout));
    setvbuf(stdin, NULL,_IONBF, 0);

    esp_vfs_dev_uart_port_set_rx_line_endings(CONFIG_ESP_CONSOLE_UART_NUM, ESP_LINE_ENDINGS_CR);
    esp_vfs_dev_uart_port_set_tx_line_endings(CONFIG_ESP_CONSOLE_UART_NUM, ESP_LINE_ENDINGS_CRLF);

    const uart_config_t uartConf = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .source_clk = UART_SCLK_REF_TICK,
    };

    uart_driver_install(CONFIG_ESP_CONSOLE_UART_NUM, 256, 0, 0, NULL, 0);
    uart_param_config(CONFIG_ESP_CONSOLE_UART_NUM, &uartConf);
    esp_vfs_dev_uart_use_driver(CONFIG_ESP_CONSOLE_UART_NUM);

    const esp_console_config_t consoleConf = {
        .max_cmdline_args = 8,
        .max_cmdline_length = 256,
    };

    esp_console_init(&consoleConf);

    linenoiseAllowEmpty(true);
    linenoiseHistorySetMaxLen(100);
}

void app_main(void){
    const char* prompt = "esp32> ";

    nvsInit();

    gpio_reset_pin(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_OUTPUT);

    consoleInit();
    esp_console_register_help_command();
    registerCommands();
    wifiInitSTA();

    xTaskCreate(&ledTask, "led_task", 1024, NULL, 5, NULL);

    printf("System Configured\n");

     printf("\n"
           "This is an example of ESP-IDF console component.\n"
           "Type 'help' to get the list of commands.\n");

    int probe_status = linenoiseProbe();
    if (probe_status) { /* zero indicates success */
        printf("\n"
               "Your terminal program does not support escape sequences.\n"
               "Line editing and history features are disabled.\n");
        linenoiseSetDumbMode(1);
    }

    while(1){
        char* line = linenoise(prompt);
        if(line==NULL){
            break;
        }

        if(strlen(line)>0){
            linenoiseHistoryAdd(line);
        }

        int ret;
        esp_err_t err = esp_console_run(line, &ret);

        if (err == ESP_ERR_NOT_FOUND) {
            printf("Unrecognized command\n");
        } else if (err == ESP_ERR_INVALID_ARG) {
            // command was empty
        } else if (err == ESP_OK && ret != ESP_OK) {
            printf("Command returned non-zero error code: 0x%x (%s)\n", ret, esp_err_to_name(ret));
        } else if (err != ESP_OK) {
            printf("Internal error: %s\n", esp_err_to_name(err));
        }

        /* linenoise allocates line buffer on the heap, so need to free it */
        linenoiseFree(line);
    }
}
