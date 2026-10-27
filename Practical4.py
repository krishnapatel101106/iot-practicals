"""
 Practical - 4

Aim: Interface RFID module with Raspberry Pi to read and write to RFID tags/cards.
Hardware Requirements
1. Raspberry Pi Model 3 B/B+
2. RFID Reader (RC 522)
3. RFID Tags or Cards
4. Jumper wires (Female to Male)
5. Breadboard

Here, I am using RFID Reader RC 522

This module came with two different styles of header pins,one of
which needed to be soldered onto the PCB.
The RFID RC522 is a very low-cost RFID (Radio-frequency
identification) reader and writer that is based on the MFRC522
microcontroller. This microcontroller provides its data throughthe
SPI protocol and works by creating a 13.56MHz electromagnetic
field that it uses to communicate with the RFID tags.

Software Requirements
1. Raspbian Stretch OS
2. SPI Supporting Libraries
3. RC522 Python Library

Connect your RFID reader with Raspberry Pi's GPIO Pins.

RFID Reader Board Pin | RPI Physical Pin |  Raspberry Function 
SDA                   |24           | GPIO8 (SPI_CE0_N)
SCK                   |23         | GPIO11 (SPI0-_CLK)
MOSI                 | 19         |GPIO10 (SPI0_MOSI)
MISO              | 21                  |GPIO9 (SPI0_MISO)
IRQ              |                  UNUSED

PREPARED BY PROF CHIRAG DEORA 2

GND 6 GND
RST 22 GPIO25 (GPIO_GEN6)
3.3V 1 3.3V PWR

Step 1: Update Raspberry Pi
    sudo apt-get update
    sudo apt-get upgrade
    sudo aspi-config

Step 2: Enable SPI Interface using sudo raspi-config tool
Select using Arrow Keys -> Interfacing Options -> SPI-> Enable

Step 3: Reboot Raspberry Pi
Step 4: Check to make sure that SPI has been enabled.type:

    lsmod | grep spi

Step 5:Install python3-dev, python3-pip packages to setting up RFID reader:
    sudo apt-get install python3-dev python3-pip

Step 6: Installspidev to Raspberry Pi using pip. The spidev library helps to handle
interactions with the SPI
    sudo pip3 install spidev

Step 7: Install the MFRC522 library using pip that helps talk to the RC522 module overthe
SPI interface
    sudo pip3 install mfrc522

Step 8: Write Python script which is used to write data from the RC522 to your RFID tags.
"""
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    text = input ('New data:')
    print("Now place you tag to write")
    reader.write(text)
    print("written")
finally:
    GPIO.cleanup()

"""
Run above script
Step 9: Write Python script which is used to read this data back off the RFID tag.
"""
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    id, text = reader.read()
    print(id)
    print(text)
finally:
    GPIO.cleanup()