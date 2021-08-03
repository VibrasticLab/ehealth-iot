#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package blueztk
Bluetoothctl GUI using tkinter
"""

# Imports
import tkinter as tk
import subprocess as sp
from tkinter import font

def btlist():
    """Bluetooth List Routine
    """
    #mfree = sp.run(["bluetoothctl","--timeout","5","scan","on"],stdout=sp.PIPE,stderr=sp.PIPE).stdout.decode("utf-8")

def teslist():
    """Test ListBox
    """
    lstbox.delete(0,tk.END)
    strlisteach = strlistbox.split('\n')
    for i in range(len(strlisteach)):
        lstbox.insert(i+1,strlisteach[i])

#sp.run(["bluetoothctl","power","on"],stdout=sp.PIPE,stderr=sp.PIPE)

## Main Window
window = tk.Tk()
window.geometry("480x320")
window.title("Tk Bluetooth")

## List Box
lstbox = tk.Listbox(window,height=10,width=25)
lstbox.pack(side=tk.LEFT, fill=tk.BOTH)

strlistbox = "Jeruk\nJambu\nPisang\nApel\nNanas"

## List Box Scrollbar
scrlstbox = tk.Scrollbar(window,width=30)
scrlstbox.pack(side=tk.LEFT,fill=tk.BOTH)

## Scrollbar Movement
lstbox.config(yscrollcommand=scrlstbox.set)
scrlstbox.config(command=lstbox.yview)

## Button Frame
btnfrm = tk.Frame(window)

## Button Bluetooth List
btnbtlist = tk.Button(btnfrm,text="  List  ",command=teslist)
btnbtlist.pack(side=tk.TOP)

## Button Tes List
btntes = tk.Button(btnfrm,text="Connect ",command=btlist)
btntes.pack(side=tk.BOTTOM)

btnfrm.pack(side=tk.RIGHT,expand=True)

## Text Font
txtfont = font.Font(window,family="Liberation Mono",size=18)
lstbox.config(font=txtfont)

## Button Font
btnfont = font.Font(btnfrm,family="Liberation Mono",size=14)
btnbtlist.config(font=btnfont)
btntes.config(font=btnfont)

window.mainloop()
