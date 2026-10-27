"""
Practical 14

Aim: Design a web dashboard using Flask. Control relay module via web. 

Hardware Requirements
1. Raspberry Pi
2. Single channel relay module
3. 3 female to female jumper wires

Connect your fingerprint sensor and relay with Raspberry Pi's GPIO Pins. 

Relay Pin |  Raspberry Pin
VCC | Pin 1(3.3V)
GND  | Pin 6 (GND)
IN  | Pin 11

Step 1: Install Flask
    sudo apt install -y python3-flask
Step 2: Create a folder structure. 
    relayweb/
    |___app.py
    |__templates/
            |__index.html
Step 3:Set the broker to start on boot
    sudo systemctl enable mosquitto
Step 4: Write the Python code. 
Code:
index.html
<html>
<body>
<button onclick="send('on')">ON</button>
<button onclick="send('off')">OFF</button>
<p id="s">OFF</p>
<script>
function send(a)
{
fetch('/'+a).then(r=>r.json()).then(d=>
{
document.getElementById('s').textContent = d.state ? 'ON':'OFF';
});
}
</script>
</body>
</html>


app.py

"""
from flask import Flask, jsonify, render_template
import RPi.GPIO as GPIO

PIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.HIGH)

app = Flask(__name__)
state = False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/on")
def on():
    global state
    GPIO.output(PIN, GPIO.LOW)
    state = True
    return jsonify(state=state)


@app.route("/off")
def off():
    global state
    GPIO.output(PIN, GPIO.HIGH)
    state = False
    return jsonify(state=state)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)