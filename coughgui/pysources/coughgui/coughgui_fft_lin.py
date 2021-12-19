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
    AudioLong = 1024
    Fs = 44100
    TitleSPL = 'RMS: 0 dB'

    def __init__(self):
        super(CoughTk, self).__init__()

        # Main Window
        self.window = tk.Tk()
        self.window.geometry("480x320")
        self.window.title("Tk CoughAnalyzer")

        # Title Label
        self.lbltitle = tk.Label(self.window, text=self.TitleSPL)
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
        self.Y = []
        self.X = []

        # Example Figure Plot
        self.fig = Figure(figsize=(5, 4), dpi=100,facecolor='black')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('black')
        self.ax.set_xlim(50,8000)
        self.ax.set_ylim([-10,120])
        self.ax.grid(True,which='both',ls='-')
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

    def rms(self,inarray,offset):
        """ Get dB SPL RMS"""

        return round(20*np.log10(np.sqrt(np.mean(np.square(inarray))))+offset,2)

    def recprocess(self):
        """ Record Process Loop"""

        unprinted = 'nan'

        while self.RecLoop:
            if self.Record:
                long, indata = self.rawinput.read()

                if long:
                    dataY = np.frombuffer(indata, dtype='i2' ) / 32768

                    if len(dataY) > 0:
                        self.Y = np.abs(np.fft.rfft(dataY))
                        self.X = np.fft.rfftfreq(len(dataY)) * self.Fs

                    self.TitleSPL = 'RMS: %5.2f dB' % (self.rms(dataY,117))
                    if not unprinted in self.TitleSPL:
                        self.lbltitle.config(text=self.TitleSPL)

    def graphupdate(self,args):
        """ Refresh Plot using new data"""

        self.line.set_data(self.X,self.Y)

if __name__ == "__main__":
    cough = CoughTk()
