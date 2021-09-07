# Raspberry Pi I/O

## WAVESHARE + I2S_MIC

| I2S-MIC | WAVESHARE | IO | NUM | NUM | IO | WAVESHARE | I2S-MIC |
|:-------:|:---------:|:--:|:---:|:---:|:--:|:---------:|:-------:|
| 3V3 | | 3V3 | 1 | 2 | 5V | 5V | |
| | | IO-2 | 3 | 4 | 5V | | |
| | | IO-3 | 5 | 6 | GND | | GND |
| | | IO-4 | 7 | 8 | IO-14 | | |
| | | GND | 9 | 10 | IO-15 | | |
| | TP_IRQ | IO-17 | 11 | 12 | IO-18 | | BCLK |
| | | IO-27 | 13 | 14 | GND | GND | |
| | | IO-22 | 15 | 16 | IO-23 | | |
| | | 3V3 | 17 | 18 | IO-24 | DC | |
| | MOSI | IO-10 | 19 | 20 | GND | | |
| | TP_MISO | IO-9 | 21 | 22 | IO-25 | RST | |
| | SCLK | IO-11 | 23 | 24 | IO-8 | CS | |
| | | GND | 25 | 26 | IO-7 | TP_CS | |
| | | IO-0 | 27 | 28 | IO-1 | | |
| | | IO-5 | 29 | 30 | GND | | |
| | | IO-6 | 31 | 32 | IO-12 | | |
| | | IO-13 | 33 | 34 | GND | | |
| WS | | IO-19 | 35 | 36 | IO-16 | | |
| |  | IO-26 | 37 | 38 | IO-20 | | DIN |
| SEL |  | GND | 39 | 40 | IO-21 | | |