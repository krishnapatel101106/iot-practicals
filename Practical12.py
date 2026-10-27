"""
Practical 12

Aim: Simulate door lock by interfacing fingerprint sensor and relay moule with
raspberry Pi. Hardware Requirements
1. Raspberry Pi
2. R307S fingerprint module
3. Single channel relay module
4. 7 female-to-female jumper wires
Connect your fingerprint sensor and relay with Raspberry Pi's GPIO Pins. 
Device           |     Wire/Pin      |RPI Physical Pin
Fingerprint     | RED      |Pin 1
Fingerprint      |BLACK      |Pin6
Fingerprint      |YELLOW      |Pin 10(RXD)
Fingerprint      |GREEN      |Pin 8(TXD)
Relay      |VCC      |Pin 17
Relay      |GND      |Pin 9
Relay      |IN      |Pin 11

Step 1: Update the system. 
    sudo apt update
Step 2: Install serial port
    sudo apt install -y python3-pip python3-serial
Step 3: Install the fingerprint library
    sudo pip3 install --break-system-packages adafruit-circuitpython-fingerprint
Step 4: Add your user to the dialout group
    sudo usermod -a -G dialout $USER
Step 5: Enable the serial port for fingerprint sensor
    sudo raspi-config
Go to Interface Options → Serial Port and answer: "Would you like a login shell to be accessible over serial?" → No
"Would you like the serial port hardware to be enabled?" → Yes
Step 6: Free up the hardware UART
    sudo nano /boot/firmware/config.txt
If the file opens empty, press Ctrl+X and use /boot/config.txt instead. Add this line at the bottom:
    dtoverlay=disable-bt
Save with Ctrl+O, press Enter, then exit with Ctrl+X. Step 7: Reboot the system
    sudo reboot
Step 8: Write the Python code. Code:
"""
import serial
import adafruit_fingerprint
import RPi.GPIO as GPIO
from time import sleep

PIN = 11
UNLOCK_TIME = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.HIGH)

uart = serial.Serial('/dev/serial0', 57600, timeout=1)
f = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def get_image():
    while f.get_image() != adafruit_fingerprint.OK:
        pass


def enroll(slot):
    print("Place finger...")
    get_image()
    f.image_2_tz(1)
    print("Remove finger")
    while f.get_image() != adafruit_fingerprint.NOFINGER:
        pass
    print("Place same finger again...")
    get_image()
    f.image_2_tz(2)
    if f.create_model() != adafruit_fingerprint.OK:
        print("Fingers did not match")
        return
    f.store_model(slot)
    print("Enrolled at slot", slot)


def unlock():
    print("ACCESS GRANTED - door unlocked")
    GPIO.output(PIN, GPIO.LOW)
    sleep(UNLOCK_TIME)
    GPIO.output(PIN, GPIO.HIGH)
    print("Door locked again")


def scan():
    print("Place finger on sensor...")
    get_image()
    f.image_2_tz(1)
    if f.finger_search() == adafruit_fingerprint.OK:
        print("Matched id", f.finger_id, "confidence", f.confidence)
        unlock()
    else:
        print("ACCESS DENIED - unknown finger")


try:
    while True:
        c = input("\n1 enroll 2 scan 3 quit: ")
        if c == "1":
            enroll(int(input("slot number: ")))
        elif c == "2":
            scan()
        elif c == "3":
            break
finally:
    GPIO.output(PIN, GPIO.HIGH)
    GPIO.cleanup()