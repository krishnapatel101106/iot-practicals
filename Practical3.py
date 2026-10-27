"""
Practical - 3

Aim: Interface TM1637 with Raspberry Pi and Display current time.

Hardware Requirements
1. Raspberry Pi Model A/B/B+
2. 4 digit 7 Segment Display
3. Jumper wires (Female to Female)

Here, I am using 4 digits-7 segments LED display with TM1637 controller

Software Requirements

1. Raspbian Stretch OS
1. Connect your 4 digit 7 segment display with Raspberry Pi's GPIO Pins.

TM1637 Board Pin  |  Function    |  RPI Physical Pin  |  Raspberry Function
GND               | Ground       |       14           |       GND
VCC               |  + 5V Power  |      4             |       5V
DI0               |Data In       | 18                 |  GPIO 24
CLK               |Clock         |     16              |GPIO 23



Step 1: Download the script using wget command.
    wget https://raspberrytips.nl/files/tm1637.py

    then you wil be in
    ~/4digitTime $ 

    write:
    ls
it will show tm1637.py

Note: This Script file contains some of the important functions, which are required to add in ourPython
script.

Note: The above script needs the tm1637.py script to work, so place both files in the same folder.

Step 2: Write Python Script to display Time (e.g clock.py)
"""
import datetime
import sys
import time
import RPi.GPIO as GPIO
import tm1637

# Initialize TM1637 Display (CLK = GPIO 23, DIO = GPIO 24)
Display = tm1637.TM1637(23, 24, tm1637.BRIGHT_TYPICAL)
Display.Clear()
Display.SetBrightness(1)  # Fixed typo: SetBrightnes -> SetBrightness

try:
    while True:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second

        # Prepare digits for the 4-digit display [H1, H2, M1, M2]
        currenttime = [
            int(hour / 10),
            hour % 10,
            int(minute / 10),
            minute % 10,
        ]

        # Update display
        Display.Show(currenttime)

        # Toggle colon point every second
        Display.ShowDoublepoint(second % 2)

        time.sleep(1)

except KeyboardInterrupt:
    # Gracefully exit on Ctrl+C
    Display.Clear()
    GPIO.cleanup()