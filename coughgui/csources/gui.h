/**
 * @file    gui.h
 * @brief   GTK GUI header.
 *
 * @addtogroup GUI
 * @{
 */

#ifndef _GUI_H_
#define _GUI_H_

#include <math.h>
#include <gtk/gtk.h>
#include <slope/slope.h>

/**
 * @brief GTK GUI construction
 * @details Call all GTK GUI build here
 */
void guiConstruct(void);

/**
 * @brief GTK GUI deconstruction
 * @details Call all GTK GUI build here
 */
void guiDeconstruct(void);

#endif

/** @} */