#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package blueztk
Bluetoothctl GUI using tkinter
"""

# Imports
import tkinter as tk
import subprocess as sp
from tkinter import font

class BtTk():
    """Bluetooth Tkinter Ccnnect class
    """

    def __init__(self):
        super(BtTk,self).__init__()

        ## Turn on Bluetooth Device
        sp.run(["bluetoothctl","power","on"],stdout=sp.PIPE,stderr=sp.PIPE)

        ## Main Window
        self.window = tk.Tk()
        self.window.geometry("480x320")
        self.window.title("Tk Bluetooth")
        self.window.config(bg="black")

        ## Title Label
        self.lbltitle = tk.Label(self.window,text="Bluetooth Connect")
        self.lbltitle.pack(side=tk.TOP)
        self.lbltitle.config(bg='black',fg='white')

        ## Status Label
        self.lblstatus = tk.Label(self.window,text="Status: Idle")
        self.lblstatus.pack(side=tk.BOTTOM)
        self.lblstatus.config(bg='black',fg='white')

        ## List Box
        self.lstbox = tk.Listbox(self.window,height=10,width=25)
        self.lstbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.lstbox.config(bg='black',fg='white')

        ## List Box V-Scrollbar
        self.vscrlstbox = tk.Scrollbar(self.window,width=30)
        self.vscrlstbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.vscrlstbox.config(bg='black')

        ## V-Scrollbar Movement
        self.lstbox.config(yscrollcommand=self.vscrlstbox.set)
        self.vscrlstbox.config(command=self.lstbox.yview)

        ## Button Frame
        self.btnfrm = tk.Frame(self.window)

        ## Button Bluetooth List
        self.btnbtlist = tk.Button(self.btnfrm,text="  List  ",command=self.btlist)
        self.btnbtlist.pack()
        self.btnbtlist.config(bg='black',fg='white')

        ## Button Bluetooth Connect
        self.btntes = tk.Button(self.btnfrm,text="Connect ",command=self.teslist)
        self.btntes.pack()
        self.btntes.config(bg='black',fg='white')

        ## Button App Quit
        self.btnquit = tk.Button(self.btnfrm,text="  Quit  ",command=self.window.destroy)
        self.btnquit.pack()
        self.btnquit.config(bg='black',fg='white')

        ## Pack Button Frame
        self.btnfrm.pack(side=tk.RIGHT,expand=True)
        self.btnfrm.config(bg='black')

        ## Text Font
        txtfont = font.Font(self.window,family="Liberation Mono",size=16)
        self.lstbox.config(font=txtfont)

        ## Button Font
        btnfont = font.Font(self.btnfrm,family="Liberation Mono",size=14)
        self.lbltitle.config(font=btnfont)
        self.lblstatus.config(font=btnfont)
        self.btnbtlist.config(font=btnfont)
        self.btntes.config(font=btnfont)
        self.btnquit.config(font=btnfont)

        ## Main Loop
        self.window.mainloop()

    def btlist(self):
        """Bluetooth List Routine
        """
        strnew = "NEW"

        self.lblstatus.config(text="Searching")
        self.lstbox.delete(0,tk.END)

        ## Get Nearby Device
        mfree = sp.run(["bluetoothctl","--timeout","5","scan","on"],stdout=sp.PIPE,stderr=sp.PIPE).stdout.decode("utf-8")

        ## Add Device List to ListBox
        eachmfree = mfree.split('\n')
        for i in range(len(eachmfree)):
            #self.lstbox.insert(i+1,eachmfree[i])
            if strnew in eachmfree[i]:
                bteach = eachmfree[i].split(" ")
                if len(bteach) > 4:
                    self.lstbox.insert(i+1, "%s %s" % (bteach[3],bteach[4]))
                else:
                    self.lstbox.insert(i+1, "%s" % (bteach[3]))
        self.lblstatus.config(text="Finished")

    def teslist(self):
        """Test ListBox
        """
if __name__ == "__main__":
    bttk = BtTk()
