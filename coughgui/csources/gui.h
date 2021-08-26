/**
 * @file    gui.h
 * @brief   GTK GUI header.
 *
 * @addtogroup GUI
 * @{
 */

#ifndef _GUI_H_
#define _GUI_H_

#include <gtk/gtk.h>

/**
 * @brief Binded some gui elements
 */ 

typedef struct{
    GtkWidget     *w_txt_vw_memory;
    GtkTextBuffer *textbuffer_main;
} app_widgets;

/**
 * @brief GTK GUI construction
 * @details Call all GTK GUI build here
 */
void guiConstruct(void);

/**
 * @brief Button memory get
 */
void on_btn_get_mem_size_clicked(GtkButton *button, app_widgets *app_wdgts);

/**
 * @brief Window destroy callback
 */
void on_window_main_destroy();

#endif

/** @} */