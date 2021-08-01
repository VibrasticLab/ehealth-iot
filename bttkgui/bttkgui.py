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
    mfree = sp.run(["bluetoothctl","--timeout","5","scan","on"],stdout=sp.PIPE,stderr=sp.PIPE).stdout.decode("utf-8")

def teslist():
    """Test ListBox
    """

sp.run(["bluetoothctl","power","on"],stdout=sp.PIPE,stderr=sp.PIPE)

## Main Window
window = tk.Tk()
window.geometry("480x320")
window.title("Tk Bluetooth")

## List Box
lstbox = tk.Listbox(window,height=10,width=40)
lstbox.pack()

lstbox.insert(1,"Bread")
lstbox.insert(2, "Milk")
lstbox.insert(3, "Meat")
lstbox.insert(4, "Cheese")
lstbox.insert(5, "Vegetables")

## Button Frame
btnfrm = tk.Frame(window)

## Button Bluetooth List
btnbtlist = tk.Button(btnfrm,text="Bluetooth List",command=btlist)
btnbtlist.pack(side=tk.LEFT)

## Button Tes List
btntes = tk.Button(btnfrm,text="Test List",command=teslist)
btntes.pack(side=tk.LEFT)

btnfrm.pack(expand=True)

## UI Font
uifont = font.Font(window,family="Liberation Mono",size=16)
lstbox.config(font=uifont)
btnbtlist.config(font=uifont)
btntes.config(font=uifont)

window.mainloop()
