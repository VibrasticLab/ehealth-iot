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

        #sp.run(["bluetoothctl","power","on"],stdout=sp.PIPE,stderr=sp.PIPE)

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

        self.strlistbox = "Jeruk\nJambu\nPisang\nApel\nNanas"

        ## List Box Scrollbar
        self.scrlstbox = tk.Scrollbar(self.window,width=30)
        self.scrlstbox.pack(side=tk.LEFT,fill=tk.BOTH)
        self.scrlstbox.config(bg='black')

        ## Scrollbar Movement
        self.lstbox.config(yscrollcommand=self.scrlstbox.set)
        self.scrlstbox.config(command=self.lstbox.yview)

        ## Button Frame
        self.btnfrm = tk.Frame(self.window)

        ## Button Bluetooth List
        self.btnbtlist = tk.Button(self.btnfrm,text="  List  ",command=self.teslist)
        self.btnbtlist.pack(side=tk.TOP)
        self.btnbtlist.config(bg='black',fg='white')

        ## Button Tes List
        self.btntes = tk.Button(self.btnfrm,text="Connect ",command=self.btlist)
        self.btntes.pack(side=tk.BOTTOM)
        self.btntes.config(bg='black',fg='white')

        self.btnfrm.pack(side=tk.RIGHT,expand=True)
        self.btnfrm.config(bg='black')

        ## Text Font
        txtfont = font.Font(self.window,family="Liberation Mono",size=18)
        self.lstbox.config(font=txtfont)

        ## Button Font
        btnfont = font.Font(self.btnfrm,family="Liberation Mono",size=14)
        self.lbltitle.config(font=btnfont)
        self.lblstatus.config(font=btnfont)
        self.btnbtlist.config(font=btnfont)
        self.btntes.config(font=btnfont)

        ## Main Loop
        self.window.mainloop()

    def btlist(self):
        """Bluetooth List Routine
        """
        #mfree = sp.run(["bluetoothctl","--timeout","5","scan","on"],stdout=sp.PIPE,stderr=sp.PIPE).stdout.decode("utf-8")

    def teslist(self):
        """Test ListBox
        """
        self.lstbox.delete(0,tk.END)
        strlisteach = self.strlistbox.split('\n')
        for i in range(len(strlisteach)):
            self.lstbox.insert(i+1,strlisteach[i])

if __name__ == "__main__":
    bttk = BtTk()
