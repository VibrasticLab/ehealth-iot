#!/bin/bash

echo 12 | sudo tee /sys/class/gpio/export
echo in | sudo tee /sys/class/gpio/gpio12/direction

echo 16 | sudo tee /sys/class/gpio/export
echo out | sudo tee /sys/class/gpio/gpio16/direction
echo 1 | sudo tee /sys/class/gpio/gpio16/value

# check button value
# gpio-12 internally pulled-down by default
#cat /sys/class/gpio/gpio12/value
