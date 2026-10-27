"""
Practical 15

Aim: Create two factor authentication system by interfacing fingerprint sensor, RFID and relay with Raspberry Pi.

Hardware Requirements
1. Raspberry Pi
2.R307S fingerprint module
3.RC522 RFID reader with card or tag
4.Single channel relay module B
5.Breadboard and jumper wires

Connect your fingerprint sensor and relay with Raspberry Pi's GPIO Pins. 
Sensor Pin | raspberry pi pin
RED         Pin 1(3.3V)
BLACK    Pin 6 (GND)
YELLOW   Pin 10 (RXD)
GREEN   Pin 8 (TXD)

Connect your RFID sensor and relay with Raspberry Pi's GPIO Pins.
Device |  Sensor Pin  | Connects to
RFID SDA Pin 24
RFID SCK Pin 23
RFID MOSI Pin 19
RFID MISO Pin 21
RFID IRQ UNUSED
RFID GND Pin 9
RFID RST Pin 22
RFID 3.3V Pin 17
Relay VCC 3.3V rail (from Pin 1)
Relay GND Pin 14 (GND)
Relay IN Pin 11 (GPIO 17)

Step 1: Update the system. 
    sudo apt update
Step 2: Install serial support
    sudo apt install -y python3-pip python3-serial
Step 3:Install the libraries
    sudo pip3 install --break-system-packages adafruit-circuitpython-fingerprint mfrc522
Step 4: Add user to the dialout group
    sudo usermod -a -G dialout $USER
Step 5: Enable the serial port for fingerprintsensor
    sudo raspi-config
Go to Interface Options → Serial Port and answer: "Would you like a login shell to be accessible over serial?" → No
"Would you like the serial port hardware to be enabled?" → Yes . Step 6: Enable SPI for RFID reader
Still in raspi-config, go to Interface Options → SPI and select Yes. Then select Finish. Step 7: Free up the hardware UART
    sudo nano /boot/firmware/config.txt
If the file opens empty, press Ctrl+X and use /boot/config.txt instead. Add this line at the bottom:
    dtoverlay=disable-bt
Save with Ctrl+O, press Enter, then exit with Ctrl+X
Step 8: Reboot the system
    sudo reboot
Step 9: Write the Python code. Code:
"""
import serial
import adafruit_fingerprint
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

PIN = 11
UNLOCK_TIME = 5

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.HIGH)

uart = serial.Serial('/dev/serial0', 57600, timeout=1)
f = adafruit_fingerprint.Adafruit_Fingerprint(uart)
reader = SimpleMFRC522()


def get_image():
    while f.get_image() != adafruit_fingerprint.OK:
        pass


def enroll(slot):
    print("Place finger...")
    get_image()
    f.image_2_tz(1)
    print("Remove finger...")
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
    print("ACCESS GRANTED - Door unlocked")
    GPIO.output(PIN, GPIO.LOW)
    sleep(UNLOCK_TIME)
    GPIO.output(PIN, GPIO.HIGH)
    print("Door locked again")


def authenticate():
    print("\n--- FACTOR 1: RFID ---")
    print("Scan your card...")
    uid, text = reader.read()
    print("UID:", uid)
    print("Card accepted")
    sleep(1)

    print("\n--- FACTOR 2: FINGERPRINT ---")
    print("Place finger...")
    get_image()
    f.image_2_tz(1)
    if f.finger_search() != adafruit_fingerprint.OK:
        print("ACCESS DENIED - Fingerprint not recognised")
        return
    print("Fingerprint accepted - ID", f.finger_id)
    unlock()


try:
    while True:
        c = input("\n1. Enroll Finger\n2. Authenticate\n3. Quit: ")
        if c == "1":
            slot = int(input("Enter slot number: "))
            enroll(slot)
        elif c == "2":
            authenticate()
        elif c == "3":
            break
finally:
    GPIO.output(PIN, GPIO.HIGH)
    GPIO.cleanup()