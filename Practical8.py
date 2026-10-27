"""
Practical 8
AIM: Interface Fingerprint Sensor with Raspberry Pi. Hardware Requirements
1. Raspberry Pi Model A/B/B+
2. FingerPrint Module
3. Breadboard
4. Jumper Wires
Connectfinderprint module with Raspberry Pi's GPIO Pins. 

Sensor Wire   |   Pin Number
Red   | Pin 1
Black   |Pin 6
Yellow   |Pin 10(RXD)
Green   |Pin 8(TXD)

Note: The blue and white wires are not used. Leave them disconnected. Step 1: Update the system
    sudo apt update
Step 2: Install serial support
    sudo apt install -y python3-pip python3-serial
Step 3: Install fingerprint library
    sudo pip3 install --break-system-packages adafruit-circuitpython-fingerprint
If it says "no such option: --break-system-packages", run it again without that flag:
    sudo pip3 install adafruit-circuitpython-fingerprint
Step 4: Add your user to the dialout group.
     sudo usermod -a -G dialout $USER
Step 5: Enable the serial port
    sudo raspi-config
Go to Interface Options → Serial Port and answer:
         "Would you like a login shell to be accessible over serial?" → No
         "Would you like the serial port hardware to be enabled?" → Yes
Step 6: Free up the hardware UART
    sudo nano /boot/firmware/config.txt
If the file opens empty, press Ctrl+X and use /boot/config.txt instead. Add this line at the
bottom of the file:
    dtoverlay=disable-bt
Save with Ctrl+O, press Enter, then exit with Ctrl+X. Step 7: Reboot the system
    sudo reboot
Step 8: Write the Python Code
Code:
"""
import adafruit_fingerprint
import serial

# Initialize serial and fingerprint sensor
uart = serial.Serial("/dev/serial0", 57600, timeout=1)
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


def verify():
    print("Place finger...")
    get_image()
    f.image_2_tz(1)
    if f.finger_search() == adafruit_fingerprint.OK:
        print("RIGHT FINGER - id", f.finger_id, "confidence", f.confidence)
    else:
        print("WRONG FINGER")


while True:
    c = input("\n1 enroll 2 verify 3 quit: ")
    if c == "1":
        enroll(int(input("slot number: ")))
    elif c == "2":
        verify()
    elif c == "3":
        break