#!/usr/bin/python
# -*- coding: utf-8 -*-

## command to record
# python alsarec.py

## command to playback
# aplay -r 44100 -f S16_LE -c 2 out.raw

import time as tm

if __name__ == "__main__":
    
    loops = 1000000
    rec_run = 0
    rec_flag = False
    
    with open("./record_status","w") as f:
        f.write('false')

    while loops > 0:
        loops -= 1

        if rec_flag:
            if rec_run > 0:
                rec_run -= 1
                print(rec_run)
            else:
                rec_flag = False
                with open("./record_status","w") as f:
                    f.write('false')
        else:
            with open("record_status", "r") as stt:
                rec_stt = stt.read()
            
            if rec_stt == 'true':
                rec_flag = True
                rec_run = 10
        
        tm.sleep(0.5)





