"""
Practical 13

Aim:Implement basic Publisher – Subscriber using MQTT. Publish messages

using paho mqtt. Subscribe and control LED. MQTT has three parts. The broker sits in the middle and passes messages along. The publisher sends a message to
a named topic. The subscriber tells the broker which topic it cares about and receives every message sent there. The publisher and subscriber never talk to each other directly — both only know the broker. In this practical all
three run on the same Raspberry Pi
Hardware Requirements
1. Raspberry Pi
2. LED
3. 1 resistor 220Ω or 330Ω
4. Breadboard and 2 jumper wires
Connect your fingerprint sensor and relay with Raspberry Pi's GPIO Pins. 
Device | Connects to
LED long leg (anode)  | Resistor → Pin 11 (GPIO 17)
LED short leg (cathode)  | Pin 6 (GND)

Step 1: Install the MQTT broker
    install -y mosquitto mosquitto-clients
Step 2: Install the Python MQTT library
    sudo pip3 install --break-system-packages paho-mqtt
Step 3:Set the broker to start on boot
    sudo systemctl enable mosquitto
Step 4: Start the broker now
    sudo systemctl start mosquitto
Step 5: Confirm whether broker running
    ystemctl status mosquitto
Look for active (running) in green. Press q to exit the status view.
Step 6: Write the Python code.
 Code:
 subscriber.py
"""
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

BROKER = "localhost"
TOPIC = "home/led"
PIN = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.LOW)


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to MQTT broker")
    print("Subscribing to:", TOPIC)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    cmd = msg.payload.decode().strip().lower()
    print("Received:", cmd)
    if cmd == "on":
        GPIO.output(PIN, GPIO.HIGH)
        print("LED ON")
    elif cmd == "off":
        GPIO.output(PIN, GPIO.LOW)
        print("LED OFF")
    else:
        print("Unknown command")


try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)

print("Subscriber running. Press Ctrl+C to stop")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber stopped.")
finally:
    GPIO.output(PIN, GPIO.LOW)
    GPIO.cleanup()

"""
publisher.py
"""
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "home/led"

try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except AttributeError:
    client = mqtt.Client()

client.connect(BROKER, 1883, 60)
client.loop_start()

print("Publisher ready.")
print("Type: on / off / quit")

try:
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "quit":
            break
        client.publish(TOPIC, cmd)
        print("Published:", cmd, "to", TOPIC)
finally:
    client.loop_stop()
    client.disconnect()
    print("Publisher closed")