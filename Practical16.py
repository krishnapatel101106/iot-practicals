"""
Practical 16

Aim: Create a motion detector by interfacing camera and 16X2 display with
Raspberry Pi. Print the appropriate message on the display.

 Hardware Requirements
1. Raspberry Pi
2. Pi Camera Module
3. 16x2 LCD display
4. One resistor, 1k to 2.2k, for contrast
5. Breadboard and jumper wires

Connect your LCD with Raspberry Pi's GPIO Pins. 
LCD Pin  | Raspberry pi pin
1 VSS   | GND rail
2 VDD |5V
3 V0  |Resistor 1k–2.2k → GND rail
4 RS | Pin 29
5 RW | GND rail
6 E  |Pin 31
11 D4  |Pin 33
12 D5 | Pin 35
13 D6  |Pin 37
14 D7  |Pin 40
15 A  |5V
16 K  |GND rail

Step 1: Update the system. 
    sudo apt update
Step 2: Install picamera and image processing packages
    sudo apt install -y python3-picamera2 python3-opencv
Step 3:Install LCD library
    sudo pip3 install --break-system-packages RPLCD
Step 4: Write
"""
import cv2
import numpy as np
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
from picamera2 import Picamera2
from time import sleep

THRESHOLD = 500000
GPIO.setwarnings(False)

# Initialize LCD (fixed syntax error by removing leading comma)
lcd = CharLCD(
    pin_rs=29,
    pin_e=31,
    pins_data=[33, 35, 37, 40],
    numbering_mode=GPIO.BOARD,
    cols=16,
    rows=2,
    dotsize=8,
)


def show(line1, line2=""):
    lcd.clear()
    lcd.write_string(line1[:16])
    if line2:
        lcd.cursor_pos = (1, 0)
        lcd.write_string(line2[:16])


show("Starting camera")
cam = Picamera2()
cam.configure(cam.create_preview_configuration(main={"size": (320, 240)}))
cam.start()
sleep(2)

show("Monitoring...", "No motion")
print("Motion detector running. Press Ctrl+C to stop.")

previous = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2GRAY)
previous = cv2.GaussianBlur(previous, (21, 21), 0)
state = False

try:
    while True:
        frame = cv2.cvtColor(cam.capture_array(), cv2.COLOR_RGB2GRAY)
        frame = cv2.GaussianBlur(frame, (21, 21), 0)
        
        diff = cv2.absdiff(previous, frame)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        score = int(np.sum(thresh))

        if score > THRESHOLD:
            if not state:
                show("MOTION", "DETECTED")
                print("MOTION DETECTED score:", score)
                state = True
        else:
            if state:
                show("Monitoring...", "No motion")
                print("No motion")
                state = False

        previous = frame
        sleep(0.3)

except KeyboardInterrupt:
    print("\nStopped")

finally:
    cam.stop()
    lcd.clear()
    lcd.close(clear=True)
    GPIO.cleanup()