#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package coughtk
CoughAnalyzer GUI using tkinter
"""

# Imports system libraries
import sys
import psutil
import tkinter as tk
import subprocess as sp
from tkinter import font

class BtTk():
    """CoughAnalyzer Program with GUI
    """

    btdeviceids = []
    play = None
    DarkTheme = False

    def __init__(self):
        super(BtTk, self).__init__()

        # Main Window
        self.window = tk.Tk()
        self.window.geometry("480x320")
        self.window.title("Tk CoughAnalyzer")

        # Title Label
        self.lbltitle = tk.Label(self.window, text="Cough Analyzer Program")
        self.lbltitle.pack(side=tk.TOP)

        # Status Label
        self.lblstatus = tk.Label(self.window, text="Program Started")
        self.lblstatus.pack(side=tk.BOTTOM)

        # Graph Box Frame
        self.graphfrm = tk.Frame(self.window)

        # Pack Listbox Frame
        self.graphfrm.pack(side=tk.LEFT, expand=True)

        # Button Frame
        self.btnfrm = tk.Frame(self.window)

        # Button Start to Analyze
        self.btnstart = tk.Button(self.btnfrm, text="  Start ")
        self.btnstart.pack()

        # Button Stop to Analyze
        self.btnstop = tk.Button(self.btnfrm, text="  Stop  ")
        self.btnstop.pack()

        # Button Graph Test
        self.btntest = tk.Button(self.btnfrm, text="  Test  ")
        self.btntest.pack()

        # Button App Quit
        self.btnquit = tk.Button(self.btnfrm, text="  Quit  ", command=self.appquit)
        self.btnquit.pack()

        # Pack Button Frame
        self.btnfrm.pack(side=tk.RIGHT, expand=True)

        # Button Font
        btnfont = font.Font(self.btnfrm, family="Liberation Mono", size=14)
        self.lbltitle.config(font=btnfont)
        self.lblstatus.config(font=btnfont)
        self.btnstart.config(font=btnfont)
        self.btnstop.config(font=btnfont)
        self.btntest.config(font=btnfont)
        self.btnquit.config(font=btnfont)

        # Dark Theme Config
        if self.DarkTheme:
            self.window.config(bg="black")
            self.lbltitle.config(bg='black', fg='white')
            self.lblstatus.config(bg='black', fg='white')
            self.graphfrm.config(bg='black')
            self.lstbox.config(bg='black', fg='white')
            self.btnstart.config(bg='black', fg='white')
            self.btnstop.config(bg='black', fg='white')
            self.btntest.config(bg='black', fg='white')
            self.btnquit.config(bg='black', fg='white')
            self.btnfrm.config(bg='black')

        # Main Loop
        self.window.mainloop()

    def isrunning(self, process):
        """ Check if a process name running"""

        for proc in psutil.process_iter():
            try:
                if process.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def appquit(self):
        """ Quit Program"""

        self.window.destroy()


if __name__ == "__main__":
    bttk = BtTk()
