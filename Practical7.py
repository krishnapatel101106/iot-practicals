"""
Practical 7

Aim:Interface 16x2 LCD with Raspberry Pi using I2C module to display text. Hardware Requirements
1. Raspberry Pi Model A/B/B+
2. 16x2 LCD
3. Breadboard
4. Jumper Wires
5. Registor(220 ohms
Connect LCD with Raspberry Pi's GPIO Pins.

LCD Pin | LCD Function | Raspberry Pi
1 VSS  GND
2 VDD  5V
3 V0   Potentiometer middle pin
4 RS   GPIO17
5 RW   GND
6 E    GPIO27
11 D4   GPIO22
12 D5    GPIO23
13 D6    GPIO24
14 D7    GPIO25
15 LED+   5V
16 LED−   GND

Step 1: Download LCD Module
Go to http://github.com/adafruit/Adafruit_Python_CharLCD and Click on Code and Download the Library for LCD. 
Once it is downloaded just extract it. Copy the whole extracted Folder and paste it in home folder(/home/pi). 

Step 2: Install the setup file
Open terminal and follow the following commands
    cd /home/pi/Adafruit_Python_CharLCD-master
    sudo python3 setup.py install

Step 3: Write the Python Code
Code:
"""
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

lcd1 = 12
lcd2 = 7
lcd3 = 8
lcd4 = 25
lcd5 = 24
lcd6 = 23

lcd = LCD.Adafruit_CharLCD(lcd1, lcd2, lcd3, lcd4, lcd5, lcd6, 0, 16, 2)
lcd.message("Welcome to LCD World!")