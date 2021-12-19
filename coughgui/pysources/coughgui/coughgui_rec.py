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
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib import style

# Import others libraries
import numpy as np
import random as rnd
from time import sleep
import alsaaudio as alsa
from threading import Thread as thd

class CoughTk():
    """CoughAnalyzer Program with GUI
    """

    Record = False
    RecLoop = True
    DarkTheme = True
    AudioLong = 512

    RecRun = 0
    RecFlag = False

    def __init__(self):
        super(CoughTk, self).__init__()

        # Create record control file
        with open("/home/alarm/record_status","w") as f:
            f.write('false')

        # Main Window
        self.window = tk.Tk()
        self.window.geometry("480x320")
        self.window.title("Tk CoughAnalyzer")

        # Title Label
        self.lbltitle = tk.Label(self.window, text="Not Recording")
        self.lbltitle.pack(side=tk.TOP)

        # Button Frame
        self.btnfrm = tk.Frame(self.window)

        # Button Start to Analyze
        self.btnstart = tk.Button(self.btnfrm, text="Start", command=self.recstart)
        self.btnstart.pack(side=tk.LEFT)

        # Button App Quit
        self.btnquit = tk.Button(self.btnfrm, text="Quit", command=self.appquit)
        self.btnquit.pack(side=tk.LEFT)

        # Pack Button Frame
        self.btnfrm.pack(side=tk.TOP)

        # Graph Frame
        self.graphfrm = tk.Frame()

        # Graph Data
        self.X = np.arange(0, 2*self.AudioLong, 1)
        self.Y = np.zeros(2*self.AudioLong, dtype='i2')

        # Example Figure Plot
        self.fig = Figure(figsize=(5, 4), dpi=100,facecolor='black')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('black')
        self.ax.set_ylim(-1,1)
        self.line, = self.ax.plot(self.X, self.Y)

        style.use('ggplot')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphfrm)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT)

        # Pack Graph Frame
        # Must packed the last
        self.graphfrm.pack(side=tk.BOTTOM,expand=True)

        # Button Font
        btnfont = font.Font(self.btnfrm, family="Liberation Mono", size=15)
        self.lbltitle.config(font=btnfont)
        self.btnstart.config(font=btnfont)
        self.btnquit.config(font=btnfont)

        # Dark Theme Config
        if self.DarkTheme:
            self.window.config(bg="black")
            self.lbltitle.config(bg='black', fg='white')
            self.btnstart.config(bg='black', fg='white')
            self.btnquit.config(bg='black', fg='white')
            self.btnfrm.config(bg='black')

        # start graph animation
        self.ani = animation.FuncAnimation(self.fig, self.graphupdate, interval=0.005, repeat=False)
        self.ani._start()

        # start mic routine
        device = 'dmic_sv'
        self.rawinput = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, channels=2, rate=44100,format=alsa.PCM_FORMAT_S16_LE, periodsize=self.AudioLong, device=device)
        thd(target=self.recprocess).start()

        # start record loop
        self.recstart()

        # Main Loop
        self.window.mainloop()

    def recstart(self):
        """ Record Process Start"""

        if self.Record:
            self.Record = False
            self.btnstart.config(text='Start')
        else:
            self.Record = True
            self.btnstart.config(text='Stop')

    def appquit(self):
        """ Program Quit"""

        self.Record = False
        self.RecLoop = False
        self.window.destroy()

    def recprocess(self):
        """ Record Process Loop"""

        while self.RecLoop:
            if self.Record:
                long, indata = self.rawinput.read()

                if long:
                    rawdata = np.frombuffer(indata, dtype='i2' )
                    self.Y = rawdata / 32768

                    if self.RecFlag:
                        if self.RecRun > 0:
                            self.RecRun -= 1
                        else:
                            self.RecFlag = False
                            RecTitle = 'Not Recording'
                            self.lbltitle.config(text=RecTitle)
                            with open("/home/alarm/record_status","w") as f:
                                f.write('false')
                    else:
                        with open("/home/alarm/record_status", "r") as stt:
                            RecStt = stt.read()

                        if RecStt == 'true':
                            self.RecRun = 100
                            RecTitle = 'RECORDING'
                            self.lbltitle.config(text=RecTitle)
                            self.RecFlag = True

                    sleep(0.01)

    def graphupdate(self,args):
        """ Refresh Plot using new data"""

        self.line.set_data(self.X,self.Y)

if __name__ == "__main__":
    cough = CoughTk()
