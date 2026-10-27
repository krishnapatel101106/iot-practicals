"""
Practical 9

Aim: Design IoT based home automation system using Raspberry Pi. Hardware Requirements
1. Raspberry Pi Model A/B/B+
2. LED
3. Breadboard
4. Jumper Wires
5. 220 Ω resistors
Connect LCD with Raspberry Pi's GPIO Pins.

LCD Pin | Device  |Raspberry Pi
1 LED 1 Pin 3
2 LED 2 Pin 5
3 LED 3 Pin 7

Step 1: Install Flask Module
Open the Raspberry Pi Terminal and install Flask. The supplied video demonstrates:

    sudo pip3 install flask

If Flask is already installed, the terminal may report that the requirement is already satisfied
Step 2: Create the Project Folder
1. Create a project directory, for example: home_automation. 
2. Inside it, create a Python file named home_automation.py. 
3. Create a subfolder named templates. 
4. Inside templates, create index.html. 
5. The Flask program will render index.html as the control page. 

Step 3: HTML Web Page – index.html
Code:

<html>
<head>
<title>Home Automation</title>
</head>
<body>
<h1>Welcome to Home Automation</h1>
<a href="/A"><button>LED 1 ON</button></a>
<a href="/a"><button>LED 1 OFF</button></a><br>
<a href="/B"><button>LED 2 ON</button></a>
<a href="/b"><button>LED 2 OFF</button></a><br>
<a href="/C"><button>LED 3 ON</button></a>
<a href="/c"><button>LED 3 OFF</button></a><br>
</body>
</html>

Note: Using host='0.0.0.0' is generally more convenient because Flask listens on available network interfaces; the Raspberry
Pi's actual IP address is then used in the browser.


Step 6: Python Flask Program – home_automation.py
"""
from flask import Flask, render_template
from flask import request
import RPi.GPIO as GPIO
import time
app = Flask(__name__)
led1 = 2
led2 = 3
led3 = 4
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
GPIO.setup(led3, GPIO.OUT)
GPIO.output(led1, 0)
GPIO.output(led2, 0)
GPIO.output(led3, 0)
print("Done")
@app.route("/")
def index():
    return render_template('index.html')
@app.route('/A')
def led1on():
    GPIO.output(led1, 1)
    return render_template('index.html')
@app.route('/a')
def led1off():
    GPIO.output(led1, 0)
    return render_template('index.html')
@app.route('/B')
def led2on():
    GPIO.output(led2, 1)
    return render_template('index.html')
@app.route('/b')
def led2off():
    GPIO.output(led2, 0)
    return render_template('index.html')
@app.route('/C')
def led3on():
    GPIO.output(led3, 1)
    return render_template('index.html')
@app.route('/c')
def led3off():
    GPIO.output(led3, 0)
    return render_template('index.html')
if __name__ == "__main__":
    print("Start")
app.run(host='0.0.0.0', port=5010)