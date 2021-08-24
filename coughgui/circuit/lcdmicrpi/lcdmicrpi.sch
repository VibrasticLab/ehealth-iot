EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr User 5906 5906
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector_Generic:Conn_02x20_Odd_Even J-RASPI1
U 1 1 61245DE1
P 3500 2500
F 0 "J-RASPI1" H 3550 3617 50  0000 C CNN
F 1 "Conn_02x20_Odd_Even" H 3550 3526 50  0000 C CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical" H 3500 2500 50  0001 C CNN
F 3 "~" H 3500 2500 50  0001 C CNN
	1    3500 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3800 1600 4000 1600
Text Label 4000 1600 0    50   ~ 0
LCD_5V
Wire Wire Line
	3800 2200 4000 2200
Text Label 4000 2200 0    50   ~ 0
LCD_GND
Wire Wire Line
	3800 2400 4000 2400
Text Label 4000 2400 0    50   ~ 0
LCD_DC
Wire Wire Line
	3800 2600 4000 2600
Text Label 4000 2600 0    50   ~ 0
LCD_RST
Wire Wire Line
	3800 2700 4000 2700
Text Label 4000 2700 0    50   ~ 0
LCD_CS
Wire Wire Line
	3800 2800 4000 2800
Text Label 4000 2800 0    50   ~ 0
LCD_TPCS
Wire Wire Line
	3300 2100 3100 2100
Text Label 3100 2100 0    50   ~ 0
LCD_TPIRQ
Wire Wire Line
	3300 2500 3100 2500
Text Label 3100 2500 0    50   ~ 0
LCD_MOSI
Wire Wire Line
	3300 2600 3100 2600
Text Label 3100 2600 0    50   ~ 0
LCD_MISO
Wire Wire Line
	3300 2700 3100 2700
Text Label 3100 2700 0    50   ~ 0
LCD_CLK
$Comp
L Connector:Conn_01x03_Female J-I2S1
U 1 1 61266362
P 1900 1650
F 0 "J-I2S1" H 1928 1676 50  0000 L CNN
F 1 "Conn_01x03_Female" H 1928 1585 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical" H 1900 1650 50  0001 C CNN
F 3 "~" H 1900 1650 50  0001 C CNN
	1    1900 1650
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x03_Female J-I2S2
U 1 1 61268738
P 1900 2050
F 0 "J-I2S2" H 1928 2076 50  0000 L CNN
F 1 "Conn_01x03_Female" H 1928 1985 50  0000 L CNN
F 2 "Connector_PinSocket_2.54mm:PinSocket_1x03_P2.54mm_Vertical" H 1900 2050 50  0001 C CNN
F 3 "~" H 1900 2050 50  0001 C CNN
	1    1900 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	1700 1550 1550 1550
Text Label 1550 1550 0    50   ~ 0
I2S_GND
Wire Wire Line
	1700 1650 1550 1650
Text Label 1550 1650 0    50   ~ 0
I2S_VDD
Wire Wire Line
	1700 1750 1550 1750
Text Label 1550 1750 0    50   ~ 0
I2S_SD
Wire Wire Line
	1700 1950 1550 1950
Text Label 1550 1950 0    50   ~ 0
I2S_LR
Wire Wire Line
	1700 2050 1550 2050
Text Label 1550 2050 0    50   ~ 0
I2S_WS
Wire Wire Line
	1700 2150 1550 2150
Text Label 1550 2150 0    50   ~ 0
I2S_SCK
Wire Wire Line
	3300 1600 3100 1600
Text Label 3100 1600 0    50   ~ 0
I2S_VDD
Wire Wire Line
	3300 3300 3100 3300
Text Label 3100 3300 0    50   ~ 0
I2S_WS
Wire Wire Line
	3800 3400 4000 3400
Text Label 4000 3400 0    50   ~ 0
I2S_SD
Wire Wire Line
	3800 2100 4000 2100
Text Label 4000 2100 0    50   ~ 0
I2S_SCK
Wire Wire Line
	3300 1700 3100 1700
Text Label 3100 1700 0    50   ~ 0
LED_0
Wire Wire Line
	3300 1800 3100 1800
Text Label 3100 1800 0    50   ~ 0
LED_1
Wire Wire Line
	3300 1900 3100 1900
Text Label 3100 1900 0    50   ~ 0
LED_2
$Comp
L Device:LED D1
U 1 1 6128A623
P 2000 2600
F 0 "D1" H 1993 2817 50  0000 C CNN
F 1 "LED" H 1993 2726 50  0000 C CNN
F 2 "LED_SMD:LED_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 2000 2600 50  0001 C CNN
F 3 "~" H 2000 2600 50  0001 C CNN
	1    2000 2600
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D2
U 1 1 6128B283
P 2000 2800
F 0 "D2" H 1993 3017 50  0000 C CNN
F 1 "LED" H 1993 2926 50  0000 C CNN
F 2 "LED_SMD:LED_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 2000 2800 50  0001 C CNN
F 3 "~" H 2000 2800 50  0001 C CNN
	1    2000 2800
	1    0    0    -1  
$EndComp
$Comp
L Device:LED D3
U 1 1 6128B923
P 2000 3000
F 0 "D3" H 1993 3217 50  0000 C CNN
F 1 "LED" H 1993 3126 50  0000 C CNN
F 2 "LED_SMD:LED_1206_3216Metric_Pad1.42x1.75mm_HandSolder" H 2000 3000 50  0001 C CNN
F 3 "~" H 2000 3000 50  0001 C CNN
	1    2000 3000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3300 3500 3100 3500
Text Label 3100 3500 0    50   ~ 0
LED_GND
Wire Wire Line
	2150 2600 2300 2600
Wire Wire Line
	2150 2800 2300 2800
Wire Wire Line
	2150 3000 2300 3000
Text Label 2300 2600 0    50   ~ 0
LED_0
Text Label 2300 2800 0    50   ~ 0
LED_1
Text Label 2300 3000 0    50   ~ 0
LED_2
Wire Wire Line
	1850 2600 1700 2600
Wire Wire Line
	1700 2600 1700 2800
Wire Wire Line
	1700 3000 1850 3000
Wire Wire Line
	1850 2800 1700 2800
Connection ~ 1700 2800
Wire Wire Line
	1700 2800 1700 3000
Wire Wire Line
	1700 2800 1600 2800
Text Label 1600 2800 0    50   ~ 0
LED_GND
Wire Wire Line
	3800 1800 4000 1800
Text Label 4000 1800 0    50   ~ 0
I2S_GND
$Comp
L Connector:Conn_01x03_Male J-I2S_LR1
U 1 1 612B4BB4
P 1900 1250
F 0 "J-I2S_LR1" H 1872 1274 50  0000 R CNN
F 1 "Conn_01x03_Male" H 1872 1183 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 1900 1250 50  0001 C CNN
F 3 "~" H 1900 1250 50  0001 C CNN
	1    1900 1250
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1700 1250 1550 1250
Text Label 1550 1250 0    50   ~ 0
I2S_LR
Wire Wire Line
	1700 1150 1550 1150
Text Label 1550 1150 0    50   ~ 0
I2S_VDD
Wire Wire Line
	1700 1350 1550 1350
Text Label 1550 1350 0    50   ~ 0
I2S_GND
$EndSCHEMATC
