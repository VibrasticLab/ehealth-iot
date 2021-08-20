#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time as tm
import tkinter as tk
import alsaaudio as alsa
from tkinter import font
from threading import Thread as thd

class TkAlsaRec():

    DarkTheme = False
    Record = False
    RecLoop = True

    def __init__(self):
        super(TkAlsaRec,self).__init__()

        self.window = tk.Tk()
        self.window.geometry("480x320")
        self.window.title('Alsa Record Test')

        self.lbltitle = tk.Label(self.window, text='Alsa Record Test')
        self.lbltitle.pack(side=tk.TOP)

        self.btnfrm = tk.Frame(self.window)

        self.btnstart = tk.Button(self.btnfrm, text='Start', command=self.recstart)
        self.btnstart.pack(side=tk.LEFT, expand=True)

        self.btnquit = tk.Button(self.btnfrm, text='Quit', command=self.appquit)
        self.btnquit.pack(side=tk.LEFT, expand=True)

        self.btnfrm.pack(side=tk.TOP, expand=True)

        if self.DarkTheme:
            self.window.config(bg="black")
            self.lbltitle.config(bg='black', fg='white')
            self.btnstart.config(bg='black', fg='white')
            self.btnquit.config(bg='black', fg='white')
            self.btnfrm.config(bg='black')

        btnfont = font.Font(self.btnfrm, family="Liberation Mono", size=20)
        self.lbltitle.config(font=btnfont)
        self.btnstart.config(font=btnfont)
        self.btnquit.config(font=btnfont)

        device = 'dmic_sv'
        self.file = open('out.raw', 'wb')
        self.rawinput = alsa.PCM(alsa.PCM_CAPTURE, alsa.PCM_NORMAL, channels=2, rate=44100,format=alsa.PCM_FORMAT_S16_LE, periodsize=512, device=device)
        thd(target=self.recprocess).start()

        self.window.mainloop()

    def recstart(self):
        if self.Record:
            self.Record = False
            if self.file:
                self.file.flush()
                self.file.close()
            self.btnstart.config(text='Start')
        else:
            if os.path.exists('out.raw'):
                os.remove('out.raw')
            self.file = open('out.raw', 'wb')

            self.Record = True
            self.btnstart.config(text='Stop')

    def appquit(self):
        self.Record = False
        self.RecLoop = False
        self.window.destroy()

    def recprocess(self):
        while self.RecLoop:
            if self.Record:
                long, indata = self.rawinput.read()

                if long:
                    if self.file:
                        self.file.write(indata)
                    tm.sleep(0.001)

if __name__ == "__main__":
    tkalsarec = TkAlsaRec()

