#!/usr/bin/python
# -*- coding: utf-8 -*-

## command to record
# bash gpio_config.sh
# python gpio_watch.py

import time as tm

if __name__ == "__main__":
    loops = 1000000
    rec_run = 0
    rec_flag = False

    while loops > 0:
        loops -= 1

        if rec_flag:
            if rec_run > 0:
                rec_run -= 1
                print(rec_run)
            else:
                with open("/sys/class/gpio/gpio12/value", "r") as stt:
                    rec_stt = stt.read().strip()

                if rec_stt == '0':
                    rec_flag = False
                    print('Record Stop')

        else:
            with open("/sys/class/gpio/gpio12/value", "r") as stt:
                rec_stt = stt.read().strip()

            if str(rec_stt) == '1':
                if rec_flag == False:
                    rec_flag = True
                    rec_run = 10
                    print('Record Start')

        tm.sleep(0.01)
