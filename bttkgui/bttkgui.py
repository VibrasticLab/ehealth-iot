#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""@package blueztk
Bluetoothctl GUI using tkinter
"""

# Imports
import tkinter as tk
import subprocess as sp

def btlist():
    """Bluetooth List Routine
    """
    txtbox.delete('1.0',tk.END)
    mfree = sp.run(["bluetoothctl","--timeout","5","scan","on"],stdout=sp.PIPE,stderr=sp.PIPE).stdout.decode("utf-8")
    txtbox.insert(tk.END,mfree)

sp.run(["bluetoothctl","power","on"],stdout=sp.PIPE,stderr=sp.PIPE)

## Main Window
window = tk.Tk()
window.geometry("480x320")
window.title("Tk MemFree")

## Text Box
txtbox = tk.Text(window,height=15,width=80)
txtbox.pack()

## Text Box Font
txtbox.config(font=("Liberation Mono",8))

## Button List
btnbtlist = tk.Button(window,text="Bluetooth List",command=btlist)
btnbtlist.pack()

window.mainloop()
