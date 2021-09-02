/**
 * @file    main.c
 * @brief   Main module code.
 *
 * @addtogroup Main
 * @{
 */

#include <gtk/gtk.h>
#include "calsa.h"
#include "gui.h"

/**
 * @brief Main function
 */
int main(int argc, char *argv[]){
    int err;

    gtk_init(&argc, &argv);

    err = calsaInit(argv[1]);
    if(err!=ALSAOK){
        fprintf(stderr,"ALSA failed\n");
        return ALSAERR;
    }
    guiConstruct();

    gtk_main();
    calsaClose();
    guiDeconstruct();

    return 0;
}

/** @} */
