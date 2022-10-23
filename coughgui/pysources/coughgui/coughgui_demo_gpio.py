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
import os
import wave
import requests
import numpy as np
import random as rnd
from time import sleep
import alsaaudio as alsa
from threading import Thread as thd

class CoughTk():
    """CoughAnalyzer Program with GUI
    """

    DarkTheme = True
    AudioLong = 1024

    RecRun = 0
    RecFlag = False

    RunGraph = True
    RunSendWav = True

    ServerTarget = "http://27.112.78.108"
    ServerName = "https://elbicare.my.id"
    EdgeIP = "0.0.0.0"

    RecFileRaw = "/home/alarm/out.raw"
    RecFileWav = "/home/alarm/out.wav"
    RecFileStatus = "/sys/class/gpio/gpio12/value"
    RecServer = ServerName + "/api/device/sendData/303"

    def __init__(self):
        super(CoughTk, self).__init__()

        # Main Window
        self.window = tk.Tk()
        self.window.geometry("320x480")
        #self.window.geometry("480x320") # if using landscape
        self.window.title("Tk CoughAnalyzer")

        # Title Label
        self.lbltitle = tk.Label(self.window, text="Cough Analyzer Prototype")
        self.lbltitle.pack(side=tk.TOP)

        # Window Font
        wndfont = font.Font(self.window, family="Liberation Mono", size=15)
        self.lbltitle.config(font=wndfont)

        # Info Frame
        self.infofrm = tk.Frame(self.window)

        # Status Connection
        self.EdgeIP = self.getwlanip()
        self.sttconn = tk.Label(self.infofrm, text=self.EdgeIP)
        self.sttconn.config(font=wndfont)
        self.sttconn.pack(side=tk.BOTTOM)

        # Start get IP loop
        thd_ip = thd(target=self.getipprocess).start()

        # Label Connection
        self.lblconn = tk.Label(self.infofrm, text="Edge-IP:")
        self.lblconn.config(font=wndfont)
        self.lblconn.pack(side=tk.BOTTOM)

        # Status Server
        self.sttserver = tk.Label(self.infofrm, text=self.ServerName)
        self.sttserver.config(font=wndfont)
        self.sttserver.pack(side=tk.BOTTOM)

        # Label Server
        self.lblserver = tk.Label(self.infofrm, text="Server:")
        self.lblserver.config(font=wndfont)
        self.lblserver.pack(side=tk.BOTTOM)

        # Send Wav Status
        txtsendwav = "Send Wav: " + "Inactive"
        self.sttsendwav = tk.Label(self.infofrm, text=txtsendwav)
        self.sttsendwav.config(font=wndfont)
        self.sttsendwav.pack(side=tk.BOTTOM)

        # Recording Status
        txtrecord = "Recording: " + "Inactive"
        self.sttrecord = tk.Label(self.infofrm, text=txtrecord)
        self.sttrecord.config(font=wndfont)
        self.sttrecord.pack(side=tk.BOTTOM)

        # Pack Info Frame
        self.infofrm.pack(side=tk.TOP)

        # Graph Frame
        self.graphfrm = tk.Frame()

        # Graph Data
        self.X = np.arange(0, 2*self.AudioLong, 1)
        self.Y = np.zeros(2*self.AudioLong, dtype='i2')

        # Example Figure Plot
        self.fig = Figure(figsize=(5, 4), dpi=100,facecolor='black')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('black')
        self.ax.grid(True,which='both',ls='-')
        self.ax.set_ylim(-1,1)
        self.line, = self.ax.plot(self.X, self.Y)

        style.use('ggplot')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphfrm)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT)

        # Pack Graph Frame
        # Must packed the last
        self.graphfrm.pack(side=tk.BOTTOM,expand=True)

        # Dark Theme Config
        if self.DarkTheme:
            self.window.config(bg="black")
            self.lbltitle.config(bg='black', fg='white')
            self.sttrecord.config(bg='black', fg='white')
            self.sttsendwav.config(bg='black', fg='white')
            self.lblserver.config(bg='black', fg='white')
            self.sttserver.config(bg='black', fg='white')
            self.lblconn.config(bg='black', fg='white')
            self.sttconn.config(bg='black', fg='white')
            self.infofrm.config(bg='black')

        # start graph animation
        self.ani = animation.FuncAnimation(self.fig, self.graphupdate, interval=0.005, repeat=False)
        self.ani._start()

        # start mic routine
        device = 'dmic_sv'
        self.rawinput = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, channels=2, rate=44100,format=alsa.PCM_FORMAT_S16_LE, periodsize=self.AudioLong, device=device)
        thd_mic = thd(target=self.recprocess).start()

        # Main Loop
        self.window.mainloop()

    def rawtowav(self):
        if os.path.exists(self.RecFileRaw):
            with open(self.RecFileRaw,"rb") as in_raw:
                rawdata = in_raw.read()
                with wave.open(self.RecFileWav,"wb") as out_wav:
                    out_wav.setparams((2, 2, 44100, 0, 'NONE', 'NONE'))
                    out_wav.writeframesraw(rawdata)

    def sendrecord(self):
        if os.path.exists(self.RecFileWav):
            files = {'file_batuk': open(self.RecFileWav,"rb")}
            values = {'nama': 'pasien', 'gender': 'unknown', 'umur': 0}
            requests.post(self.RecServer,files=files, data=values)

    def getwlanip(self):
        ipv4 = os.popen('ip addr show wlan0 | grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'').read().strip()
        return ipv4

    def getipprocess(self):
        """Get IP Loop"""

        while True:
            self.EdgeIP = self.getwlanip()
            sleep(5)

    def recprocess(self):
        """ Record Process Loop"""

        while True:
            long, indata = self.rawinput.read()

            if long:
                self.Y = np.frombuffer(indata, dtype='i2' ) /32768

                if self.RecFlag:
                    if self.RecRun > 0:
                        self.RecRun -= 1
                        self.RawOut.write(indata)
                    else:
                        self.RecFlag = False
                        self.RunGraph = False
                        self.RawOut.flush()
                        self.RawOut.close()

                        txtrecord = "Recording: " + "Convert"
                        self.sttrecord.config(text=txtrecord)
                        self.rawtowav()
                        txtrecord = "Recording: " + "Inactive"
                        self.sttrecord.config(text=txtrecord)

                        txtsendwav = "Send Wav: " + "Active"
                        self.sttsendwav.config(text=txtsendwav)
                        if self.RunSendWav:
                            self.sendrecord()
                        txtsendwav = "Send Wav: " + "Inactive"
                        self.sttsendwav.config(text=txtsendwav)

                        self.RunGraph = True
                else:
                    with open(self.RecFileStatus, "r") as stt:
                        RecStt = stt.read().strip()

                    if RecStt == '1':
                        self.RecRun = 200 # 3 seconds recording
                        txtrecord = "Recording: " + "Active"
                        self.sttrecord.config(text=txtrecord)
                        with open(self.RecFileRaw,"w") as out:
                            out.write('')
                        self.RawOut = open(self.RecFileRaw, "wb")
                        self.RecFlag = True

                sleep(0.01)

    def graphupdate(self,args):
        """ Refresh Plot using new data"""

        if self.RunGraph:
            self.line.set_data(self.X,self.Y)

if __name__ == "__main__":
    cough = CoughTk()
