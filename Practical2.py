"""
Practical - 2
Aim: Use Telegram to control Raspberry Pi GPIO.

Hardware Requirements
1. Raspberry Pi Model A/B/B+
2. LED
3. Breadboard
4. Jumper Wires
5. Registor
Connect LED with Raspberry Pi's GPIO Pins.
    ________________________________________________________________
    | Led Terminal     | Pin Number         |   GPIO Number         |
    ----------------------------------------------------------------    
    |Led Positive      |     Pin 1 1       |  GPIO 17               |
    |Led Negative      |    Pin 0 6        |  Ground                |
    ________________________________________________________________

    
Step 1: Install Telegram on Your Phone, Obviously

Go to App Store (iPhone) or Play Store (Android), download and install Telegram on your phone. Now, you can
use Telegram. Not yet for the Raspberry Pi. Telegram reserves a special kind of accounts for machines, called bot
accounts. As the owner of your own Pi, you have to obtain a bot account for it.

Step 2: Text /newbot to BotFather
Open Telegram on your phone, search for a user called BotFather. As the name implies, he is the Father of All
Bots. He accepts special commands, because he does not understand plain English very well.
To obtain a bot account, text him /newbot. (you need the slash '/' in front) He will then ask a couple of questions. I
call my bot "Led”. You will see why in a few moments. But you can give it any name you want.
At the end of process, you will be given a token, something like 123456789:ABCdefGhIJKlmNo-PQRsTUVwxyZ. This
token represents the bot account. You are going to put this token on the Pi.

Step 3: Install Telepot on Raspberry Pi

On the command line, run these two commands: sudo apt-get

        install python-pip
        sudo pip install telepot

Step 4: Test Token
On the command line, type python to enter the Python interpreter. In thePython interpreter, enter these three lines;

        import teleport
        bot = telepot.Bot('*** copy bot token from botfather ***')
        bot.getMe()

You should keep bot token secret too. Having the token means having access to the bot account.
If the last command, getMe(), returns a dictionary describing the bot account (as in the screenshot), all is good.
Type exit() to leave the Python interpreter.
If not, you have copied the wrong token. Type exit() to leave the Python interpreter. Then type python to come in again, and
repeat those three lines of code.


Step 5: Write the Python Code
Code:

"""
import sys import time
import random import
datetime import telepot
import RPi.GPIO as GPIO
from telepot.loop import MessageLoop

red=23 # connect red led at pin 23 of raspberry pi

now=datetime.datetime.now()
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(red,GPIO.OUT) 
GPIO.output(red,0)

def action(msg):
    chat_id = msg['chat']['id'] 
    command = msg['text']

    print ('Got command: %s' %command)
    
    if 'On' in command:
        message="Turn On" 
        message=message+"red"
        GPIO.output(red,1)
        bot.sendMessage(chat_id,message)
    
    if 'Off' in command:
        message="Turn Off" 
        message=message+" red"
        GPIO.output(red,0) 
        bot.sendMessage(chat_id,message)

bot = telepot.Bot('626665131:AAHsNzQbqSj9GZ9-w2t4I') #paste your bot tokan here.
print(bot.getMe())
MessageLoop(bot,action).run_as_thread() 
print('I am listening...')

while 1:
    time.sleep(10)