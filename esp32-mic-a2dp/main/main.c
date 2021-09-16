#include "my_nvs.h"
#include "my_led.h"
#include "my_cmd.h"
#include "my_shell.h"
#include "my_wifista.h"
#include "myconfig.h"

void app_main(void){
    nvsInit();
    ledInit();
    wifiInitSTA();
    shellInit();

    while(1){
        int loop = shellLoop();
        if(loop==1)break;
    }
}
