#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package blueztk
Bluetoothctl GUI using tkinter
"""

# Imports system libraries
import sys
import psutil
import tkinter as tk
import subprocess as sp
from tkinter import font

# Imports local libraries
sys.path.append(".")
from btctlwrapper import BluetoothctlWrapper

class BtTk():
    """Bluetooth Tkinter Connect class
    """

    btdeviceids = []
    play = None
    DarkTheme = False

    def __init__(self):
        super(BtTk, self).__init__()

        # Bluetoothctl Wrapper object
        self.btctl = BluetoothctlWrapper()

        # Main Window
        self.window = tk.Tk()
        self.window.geometry("480x320")
        self.window.title("Tk Bluetooth")

        # Title Label
        self.lbltitle = tk.Label(self.window, text="Bluetooth Audio Connect")
        self.lbltitle.pack(side=tk.TOP)

        # Status Label
        self.lblstatus = tk.Label(self.window, text="Bluetooth Started")
        self.lblstatus.pack(side=tk.BOTTOM)

        # List Box Frame
        self.lstfrm = tk.Frame(self.window)

        # List Box H-Scrollbar
        self.hscrlstbox = tk.Scrollbar(self.lstfrm, width=30, orient="horizontal")
        self.hscrlstbox.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # List Box V-Scrollbar
        self.vscrlstbox = tk.Scrollbar(self.lstfrm, width=30)
        self.vscrlstbox.pack(side=tk.RIGHT, fill=tk.BOTH)

        # List Box
        self.lstbox = tk.Listbox(self.lstfrm, height=10, width=25)
        self.lstbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # V-Scrollbar Movement
        self.lstbox.config(yscrollcommand=self.vscrlstbox.set)
        self.vscrlstbox.config(command=self.lstbox.yview)

        # H-Scrollbar Movement
        self.lstbox.config(xscrollcommand=self.hscrlstbox.set)
        self.hscrlstbox.config(command=self.lstbox.xview)

        # Pack Listbox Frame
        self.lstfrm.pack(side=tk.LEFT, expand=True)

        # Button Frame
        self.btnfrm = tk.Frame(self.window)

        # Button Play a MP3
        self.btnplay = tk.Button(self.btnfrm, text="  Play  ", command=self.playstart)
        self.btnplay.pack()

        # Button Stop a MP3
        self.btnstop = tk.Button( self.btnfrm, text="  Stop  ", command=self.playstop)
        self.btnstop.pack()

        # Button Bluetooth List
        self.btnbtlist = tk.Button(self.btnfrm, text="  List  ", command=self.btlist)
        self.btnbtlist.pack()

        # Button Bluetooth Paired
        self.btnpair = tk.Button(self.btnfrm, text="Paired", command=self.btpaired)
        self.btnpair.pack()

        # Button Bluetooth Connect
        self.btnconn = tk.Button(self.btnfrm, text="Connect ", command=self.btconnect)
        self.btnconn.pack()

        # Button Pulseaudio Restart
        self.btnplse = tk.Button(self.btnfrm, text="PulseRST", command=self.pulserst)
        self.btnplse.pack()

        # Button App Quit
        self.btnquit = tk.Button(self.btnfrm, text="  Quit  ", command=self.appquit)
        self.btnquit.pack()

        # Pack Button Frame
        self.btnfrm.pack(side=tk.RIGHT, expand=True)

        # Text Font
        txtfont = font.Font(self.window, family="Liberation Mono", size=18)
        self.lstbox.config(font=txtfont)

        # Button Font
        btnfont = font.Font(self.btnfrm, family="Liberation Mono", size=14)
        self.lbltitle.config(font=btnfont)
        self.lblstatus.config(font=btnfont)
        self.btnplay.config(font=btnfont)
        self.btnstop.config(font=btnfont)
        self.btnbtlist.config(font=btnfont)
        self.btnpair.config(font=btnfont)
        self.btnconn.config(font=btnfont)
        self.btnplse.config(font=btnfont)
        self.btnquit.config(font=btnfont)

        # Dark Theme Config
        if self.DarkTheme:
            self.window.config(bg="black")
            self.lbltitle.config(bg='black', fg='white')
            self.lblstatus.config(bg='black', fg='white')
            self.hscrlstbox.config(bg='black')
            self.vscrlstbox.config(bg='black')
            self.lstfrm.config(bg='black')
            self.lstbox.config(bg='black', fg='white')
            self.btnplay.config(bg='black', fg='white')
            self.btnstop.config(bg='black', fg='white')
            self.btnbtlist.config(bg='black', fg='white')
            self.btnpair.config(bg='black', fg='white')
            self.btnconn.config(bg='black', fg='white')
            self.btnplse.config(bg='black', fg='white')
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

    def btlist(self):
        """Bluetooth List Routine
        """

        self.lstbox.delete(0, tk.END)
        self.btdeviceids.clear()

        self.btctl.start_scan()
        scan_result = self.btctl.get_available_devices()

        for i in range(len(scan_result)):
            self.btdeviceids.append(scan_result[i]['mac_address'])
            self.lstbox.insert(i+1, "%s" % (scan_result[i]['name']))

        self.lblstatus.config(text="Available List")

    def btpaired(self):
        """Bluetooth List Routine
        """

        self.lstbox.delete(0, tk.END)
        self.btdeviceids.clear()

        pair_result = self.btctl.get_paired_devices()

        for i in range(len(pair_result)):
            self.btdeviceids.append(pair_result[i]['mac_address'])
            self.lstbox.insert(i+1, "%s" % (pair_result[i]['name']))

        self.lblstatus.config(text="Paired List")

    def btconnect(self):
        """Connect Bluetooth
        """
        
        if len(self.btdeviceids) > 0:
            if self.lstbox.curselection():
                idselect = self.lstbox.curselection()[0]
                if self.btdeviceids[idselect]:
                    self.lblstatus.config(
                        text="Connected: " + self.btdeviceids[idselect])

                    sp.check_output("pulseaudio --start", shell=True)

                    btdevid = self.btdeviceids[idselect]
                    self.btctl.pair(btdevid)
                    self.btctl.connect(btdevid)
                    self.btctl.trust(btdevid)

        else:
            self.lblstatus.config(text="List First")

    def pulserst(self):
        """ Restart Pulseaudio Server"""

        sp.check_output("pulseaudio -k", shell=True)
        sp.check_output("pulseaudio --start", shell=True)
        self.lblstatus.config(text="Pulseaudio restarted")

    def playstart(self):
        """ Start a MP3 player"""

        self.playstop()
        self.play = sp.Popen(
            ["play", "-q", "-v", "0.05", "~/arcv-kirifuda.mp3"], stdout=None, stderr=None)

    def playstop(self):
        """ Stop a MP3 player"""

        if not (self.play is None):
            self.play.terminate()

    def appquit(self):
        """ Quit Program"""

        self.playstop()
        self.window.destroy()


if __name__ == "__main__":
    bttk = BtTk()
