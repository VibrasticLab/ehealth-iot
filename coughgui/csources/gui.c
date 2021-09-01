/**
 * @file    gui.c
 * @brief   GTK GUI code.
 *
 * @addtogroup GUI
 * @{
 */

#include "gui.h"
#include "calsa.h"
#include <stdio.h>

SlopeScale* scale;
SlopeItem* series;

double* x;
double* y;
const long n = BUFFERFRAME;
GtkWidget* chart;

/* Audio buffer */
short audioBuffer[BUFFERFRAME];

gboolean timer_cb(GtkWidget* chart){
    int err;
    unsigned int k;

    err=calsaInput(audioBuffer);
    if(err!=ALSAOK)return TRUE;

    for(k=0;k<n;++k){
        y[k] = (double) audioBuffer[k]/PCMSCALE;
    }

    slope_xyseries_set_data(SLOPE_XYSERIES(series), x, y, n);
    slope_chart_redraw(SLOPE_CHART(chart));

    return TRUE;
}

void guiConstruct(void){
    chart = slope_chart_new();
    g_signal_connect(G_OBJECT(chart), "destroy", G_CALLBACK(gtk_main_quit), NULL);

    x = g_malloc(n * sizeof(double));
    y = g_malloc(n * sizeof(double));

    long k;
    for (k = 0; k < n; ++k){
      x[k] = k;
      y[k] = (double) 2*sin(2*M_PI*x[k]/BUFFERFRAME);
    }

    scale = slope_xyscale_new();
    slope_chart_add_scale(SLOPE_CHART(chart), scale);

    series = slope_xyseries_new_filled("wave", x, y, n, "b-");
    slope_scale_add_item(scale, series);

    g_timeout_add(10, (GSourceFunc) timer_cb, (gpointer) chart);

    gtk_widget_set_size_request(chart, 480, 320);
    gtk_window_set_resizable(GTK_WINDOW(chart), FALSE);
    gtk_window_set_decorated(GTK_WINDOW(chart), FALSE);

    gtk_widget_show_all(chart);
}

void guiDeconstruct(void){
    g_free(x);
    g_free(y);
}

/** @} */
