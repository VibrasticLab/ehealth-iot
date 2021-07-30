#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import subprocess as sp

def memfree():
    txtbox.delete('1.0',tk.END)
    mfree = sp.run(["bluetoothctl","--timeout","5","scan","on"],stdout=sp.PIPE,stderr=sp.PIPE).stdout.decode("utf-8")
    txtbox.insert(tk.END,mfree)

sp.run(["bluetoothctl","power","on"],stdout=sp.PIPE,stderr=sp.PIPE)

window = tk.Tk()
window.geometry("480x320")
window.title("Tk MemFree")

txtbox = tk.Text(window,height=15,width=80)
txtbox.config(font=("Liberation Mono",8))
txtbox.pack()

btnmem = tk.Button(window,text="Bluetooth List",command=memfree)
btnmem.pack()

window.mainloop()
