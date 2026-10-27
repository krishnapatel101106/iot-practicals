"""
Practical 11

Aim: Interface Fingerprint Sensor and 16X2 LCD with Raspberry and display
message RFID UID matched or unmatched.

Hardware Requirements
1. 2. 3. 4. 5. 6.
Raspberry Pi
fingerprint module
RC522 RFID reader with card or tag
16x2 LCD display (parallel, non-I2C)
One resistor,1k to 2.2k, for contrast
Breadboard and jumper wire

Connect your fingerprint sensor with Raspberry Pi's GPIO Pins.
Sensor Wire  | RPI Physical Pin
RED 1
BLACK 6
YELLOW 10(RXD)
GREEN 8(TXD)

Connect your RFID sensor with Raspberry Pi's GPIO Pins.
Sensor Wire  | RPI Physical Pin
SDA 24
SCK 23
MOSI 19
MISO 21
IRQ Unused
GND 9
RST 22
3.3V 17

Connect your 16x2 LCD with Raspberry Pi's GPIO Pins.
Sensor Wire   | Connects to
1 VSS     |GND rail
2 VDD    | 5V
3 V0     |Resistor 1k–2.2k → GND rail
4 RS     |Pin29
5 RW     |GND rail
6 E     |Pin 31
11 D4     |Pin 33
12 D5     |Pin 35
13 D6     |Pin 37
14 D7     |Pin 40
15 A     |5V
16 K     |GND rail

Step 1: Update the system.
     sudo apt update
Step 2: Write Python Script to display Time (e.g clock.py)
    sudo apt install -y python3-pip python3-serial
Step 3: Install three libraries
    sudo pip3 install --break-system-packages adafruit-circuitpython-fingerprint mfrc522 RPLCD
Step 4: Add your user to the dialout group
    sudo usermod -a -G dialout $USER
Step 5: Enable the serial port for fingerprint sensor
    sudo raspi-config
Go to Interface Options → Serial Port and answer: "Would you like a login shell to be accessible over serial?" → No
"Would you like the serial port hardware to be enabled?" → Yes
Step 6: Enable SPI for RFID reader
Still in raspi-config, go to Interface Options → SPI and select Yes. Then select Finish. Step 7: Free up the hardware UART
    sudo nano /boot/firmware/config.txt
If the file opens empty, press Ctrl+X and use /boot/config.txt instead. Add this line at the bottom:
    dtoverlay=disable-bt
Save with Ctrl+O, press Enter, then exit with Ctrl+X. Step 8: Reboot the system
    sudo reboot
Step 9: Write
"""
import serial
import adafruit_fingerprint
import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
from mfrc522 import SimpleMFRC522
from time import sleep

ALLOWED_TAGS = [695924236005]
GPIO.setwarnings(False)

# Initialize LCD and Serial/Sensors
lcd = CharLCD(
    pin_rs=29,
    pin_e=31,
    pins_data=[33, 35, 37, 40],
    numbering_mode=GPIO.BOARD,
    cols=16,
    rows=2,
    dotsize=8,
)
uart = serial.Serial('/dev/serial0', 57600, timeout=1)

f = adafruit_fingerprint.Adafruit_Fingerprint(uart)
reader = SimpleMFRC522()


def show(line1, line2=""):
    lcd.clear()
    lcd.write_string(line1[:16])
    if line2:
        lcd.cursor_pos = (1, 0)
        lcd.write_string(line2[:16])


def get_image():
    while f.get_image() != adafruit_fingerprint.OK:
        pass


def enroll(slot):
    show("Place finger")
    print("Place finger...")
    get_image()
    f.image_2_tz(1)
    show("Remove finger")
    print("Remove finger")
    while f.get_image() != adafruit_fingerprint.NOFINGER:
        pass
    show("Place again")
    print("Place same finger again...")
    get_image()
    f.image_2_tz(2)
    if f.create_model() != adafruit_fingerprint.OK:
        show("Did not match", "Try again")
        print("Fingers did not match")
        sleep(2)
        return
    f.store_model(slot)
    show("Enrolled", "Slot" + str(slot))
    print("Enrolled at slot", slot)
    sleep(2)


def scan_finger():
    show("Place finger")
    print("Place finger...")
    get_image()
    f.image_2_tz(1)
    if f.finger_search() == adafruit_fingerprint.OK:
        show("FINGER MATCHED", " ID " + str(f.finger_id))
        print("FINGER MATCHED - id", f.finger_id)
    else:
        show("FINGER", "UNMATCHED")
        print("FINGER UNMATCHED")
    sleep(3)


def scan_rfid():
    show("Scan RFID card")
    print("Scan RFID card...")
    uid, text = reader.read()
    print("UID:", uid)
    if uid in ALLOWED_TAGS:
        show("UID MATCHED", str(uid))
        print("UID MATCHED")
    else:
        show("UID UNMATCHED", str(uid))
        print("UID UNMATCHED")
    sleep(3)


try:
    show("System ready")
    sleep(2)
    while True:
        c = input("\n1 enroll finger 2 scan finger 3 scan RFID 4 quit: ")
        if c == "1":
            enroll(int(input("slot number: ")))
        elif c == "2":
            scan_finger()
        elif c == "3":
            scan_rfid()
        elif c == "4":
            break
    show("System ready")
finally:
    lcd.clear()
    lcd.close(clear=True)
    GPIO.cleanup()