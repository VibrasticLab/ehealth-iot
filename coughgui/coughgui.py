#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package coughtk
CoughAnalyzer GUI using tkinter
"""

# Imports system libraries
import tkinter as tk
from tkinter import font

# Import matplotlib libraries
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib import style

import numpy as np
import random as rnd

from time import sleep
from threading import Timer as tmr
from threading import Thread as thd

class CoughTk():
    """CoughAnalyzer Program with GUI
    """

    loopdata = False
    loopgraph = False
    DarkTheme = False

    def __init__(self):
        super(CoughTk, self).__init__()

        # Main Window
        self.window = tk.Tk()
        self.window.geometry("480x320")
        self.window.title("Tk CoughAnalyzer")

        # Title Label
        self.lbltitle = tk.Label(self.window, text="Cough Analyzer Program")
        self.lbltitle.pack(side=tk.TOP)

        # Button Frame
        self.btnfrm = tk.Frame(self.window)

        # Button Start to Analyze
        self.btnstart = tk.Button(self.btnfrm, text=" Start/Stop", command=self.randomtest)
        self.btnstart.pack(side=tk.LEFT)

        # Button Graph Test
        self.btntest = tk.Button(self.btnfrm, text="  Test  ")
        self.btntest.pack(side=tk.LEFT)

        # Button App Quit
        self.btnquit = tk.Button(self.btnfrm, text="  Quit  ", command=self.appquit)
        self.btnquit.pack(side=tk.LEFT)

        # Pack Button Frame
        self.btnfrm.pack(side=tk.TOP)

        # Graph Frame
        self.graphfrm = tk.Frame()

        # Graph Data
        self.F = 5
        self.t = np.arange(0, 3, .01)
        self.y = np.sin(self.F * np.pi * self.t)

        # Example Figure Plot
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylim(-1,1)
        self.line, = self.ax.plot(self.t, self.y)

        style.use('ggplot')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphfrm)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT)

        self.canvas.mpl_connect("key_press_event", self.on_key_press)

        # Pack Graph Frame
        # Must packed the last
        self.graphfrm.pack(side=tk.BOTTOM,expand=True)

        # Button Font
        btnfont = font.Font(self.btnfrm, family="Liberation Mono", size=15)
        self.lbltitle.config(font=btnfont)
        self.btnstart.config(font=btnfont)
        self.btntest.config(font=btnfont)
        self.btnquit.config(font=btnfont)

        # Dark Theme Config
        if self.DarkTheme:
            self.window.config(bg="black")
            self.lbltitle.config(bg='black', fg='white')
            self.btnstart.config(bg='black', fg='white')
            self.btntest.config(bg='black', fg='white')
            self.btnquit.config(bg='black', fg='white')
            self.btnfrm.config(bg='black')

        # start graph loop
        self.loopgraph = True
        thd(target=self.graphloop).start()

        # Main Loop
        self.window.mainloop()

    def on_key_press(self,event):
        """ Test Graph Key Event"""

        key_press_handler(event, self.canvas)

    def appquit(self):
        """ Quit Program"""

        self.loopdata = False
        self.loopgraph = False
        self.window.destroy()

    def randomtest(self):
        if self.loopdata:
            self.loopdata = False
        else:
            self.loopdata = True
            self.randomfreq()

    def randomfreq(self):
        """ Update Data with random frequency"""

        self.F = rnd.randint(5,20)
        self.y = np.sin(self.F* np.pi * self.t)
        print("update")

        if self.loopdata:
            tmr(0.1,self.randomfreq).start()

    def graphloop(self):
        """ Refresh Plot using new data"""

        while self.loopgraph:
            self.graphdraw()
            sleep(0.005)

    def graphdraw(self):
        """ Refresh Plot using new data"""

        self.line.set_data(self.t,self.y)
        self.canvas.draw_idle()

if __name__ == "__main__":
    cough = CoughTk()
