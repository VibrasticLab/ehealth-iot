#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/portmacro.h"
#include "freertos/projdefs.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_err.h"

#include "lwip/err.h"
#include "lwip/sys.h"

#include "my_wifista.h"

#define ESP_WIFI_SSID "vibrastic"
#define ESP_WIFI_PASS "bismillah"
#define ESP_WIFI_RETRY 5

#define WIFI_CONNECTED_BIT  BIT0
#define WIFI_FAIL_BIT       BIT1

static EventGroupHandle_t wifiEventGroup;
static int wifiRetryNum = 0;

static void eventHandler(void* arg, esp_event_base_t event_base, int32_t event_id, void* event_data){
    if(event_base==WIFI_EVENT && event_id==WIFI_EVENT_STA_START){
        esp_wifi_connect();
    }
    else if (event_base==WIFI_EVENT && event_id==WIFI_EVENT_STA_DISCONNECTED){
        if(wifiRetryNum<ESP_WIFI_RETRY){
            esp_wifi_connect();
            wifiRetryNum++;
            printf("retry to connect WiFi\n");
        }
        else{
            xEventGroupSetBits(wifiEventGroup,WIFI_FAIL_BIT);
        }
        printf("connect WiFi failed\n");
    }
    else if (event_base==IP_EVENT && event_id==IP_EVENT_STA_GOT_IP){
        ip_event_got_ip_t* eventIP = (ip_event_got_ip_t*) event_data;
        printf("Got IP: " IPSTR, IP2STR(&eventIP->ip_info.ip));
        wifiRetryNum = 0;
        xEventGroupSetBits(wifiEventGroup, WIFI_CONNECTED_BIT);
        printf("\n");
    }
}

void wifiInitSTA(void){
    wifiEventGroup = xEventGroupCreate();

    ESP_ERROR_CHECK(esp_netif_init());

    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t wifiInitConf = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&wifiInitConf));

    esp_event_handler_instance_t instAnyID;
    esp_event_handler_instance_t instGotIP;

    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
                                                        ESP_EVENT_ANY_ID,
                                                        &eventHandler,
                                                        NULL,
                                                        &instAnyID));

    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT,
                                                        IP_EVENT_STA_GOT_IP,
                                                        &eventHandler,
                                                        NULL,
                                                        &instGotIP));

    wifi_config_t wifiConf = {
        .sta = {
            .ssid = ESP_WIFI_SSID,
            .password = ESP_WIFI_PASS,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifiConf));
    ESP_ERROR_CHECK(esp_wifi_start());

    printf("Wifi Started \n");

    EventBits_t bits = xEventGroupWaitBits(wifiEventGroup,
                                            WIFI_CONNECTED_BIT | WIFI_FAIL_BIT,
                                            pdFALSE,
                                            pdFALSE,
                                            portMAX_DELAY);

    if (bits & WIFI_CONNECTED_BIT){
        printf("WiFi connect Success %s\n", ESP_WIFI_SSID);
    }
    else if(bits & WIFI_FAIL_BIT){
        printf("WiFi connect Fail %s\n", ESP_WIFI_SSID);
    }
    else{
        printf("Unexpexted Event \n");
    }

    ESP_ERROR_CHECK(esp_event_handler_instance_unregister(IP_EVENT, IP_EVENT_STA_GOT_IP, &instGotIP));
    ESP_ERROR_CHECK(esp_event_handler_instance_unregister(WIFI_EVENT, ESP_EVENT_ANY_ID, &instAnyID));
    vEventGroupDelete(wifiEventGroup);
}

