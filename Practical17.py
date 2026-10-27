"""
Practical 17

Aim:Write a program to read the CPU%, Memory% and CPU temperature of Raspberry Pi.

 Hardware Requirements
1. Raspberry Pi 4B
2. MicroSD Card with Raspberry Pi OS
3. Power Supply
4. Keyboard and Mouse (or SSH connection)
5. Ethernet cable


Software Requirements
1. Python 3
2. psutil Python library

Step 1: Install the Required Library
Open the Terminal and install psutil using the following command
    sudo apt update
    sudo apt install -y python3-psutil
Step 2: Write the Python Program
"""
import psutil
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
        temperature = int(file.read()) / 1000
    return temperature
print("Raspberry Pi System Monitor")
print("---------------------------")
cpu_percent = psutil.cpu_percent(interval=1)
memory_percent = psutil.virtual_memory().percent
cpu_temperature = get_cpu_temperature()
print(f"CPU Usage : {cpu_percent}%")
print(f"Memory Usage : {memory_percent}%")
print(f"CPU Temperature : {cpu_temperature:.2f} °C")
print("---------------------------")