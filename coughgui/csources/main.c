/**
 * @file    main.c
 * @brief   Main module code.
 *
 * @addtogroup Main
 * @{
 */

#include <gtk/gtk.h>
#include "gui.h"

/**
 * @brief Main function
 */
int main(int argc, char *argv[]){
    gtk_init(&argc, &argv);
    guiConstruct();
    gtk_main();
    guiDeconstruct();
    return 0;
}

/** @} */