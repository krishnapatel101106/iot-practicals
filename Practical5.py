"""
Practical 5

AIM: Interface Pi Camera with Raspberry Pi to capture image and video.


Hardware Requirements
➢ Raspberry Pi , SD Card
➢ Pi camera
➢ Power supply
➢ Ethernet Cable / Wi Fi
➢ Monitor , Keyboard, Mouse (Optional ,For without headless connection)

Software Requirements
➢ Raspbian Stretch OS
➢ Python Script

System Explanation
➢ Pi camera is used to capture the images and record the videos of visitors, when a push button is pressed or triggered.
➢ After pushing the one button, Raspberry Pi sends command to Pi Camera to click the picture and save it.
➢ Similarly, after pushing another button, Raspberry Pi sends command to Pi Camera to record the video and save it.
➢ The buzzer is used to generate sound when button pressed.

Step 1: Connect the camera
Switch OFF the Raspberry Pi before connecting the ribbon cable.
On Raspberry Pi 4, locate the CSI camera connector. The ribbon cable has a blue side and contacts.
Make sure the cable is fully inserted and the connector latch is secured.
Then power ON the Raspberry Pi.

Step 2: Update Raspberry Pi OS
    sudo apt update
    sudo apt full-upgrade -y
    sudo reboot

Step 3: Check whether the camera is detected
On recent Raspberry Pi OS versions, run:
    rpicam-hello

If the camera is detected, you should get a camera preview.

Step 4: Install Picamera2
    For Python programming, install Picamera2:
        sudo apt update
        udo apt install -y python3-picamera2
    Also install the preview dependencies:
        sudo apt install -y python3-libcamera python3-kms++
    Check that Picamera2 is installed:
        python3 -c "from picamera2 import Picamera2; print('Picamera2 OK')"
Picamera2 OK

Step 5: Python program to capture an image
"""
from picamera2 import Picamera2
from time import sleep
picam2 = Picamera2() # Initialize camera
config = picam2.create_still_configuration() # Configure camera for still capture
picam2.configure(config)
picam2.start()
sleep(2) # Let camera adjust exposure
picam2.capture_file("image.jpg")
picam2.stop()
print("Image captured and saved as image.jpg")

"""
Step 6: Python program to capture video
"""
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from time import sleep
picam2 = Picamera2()
video_config = picam2.create_video_configuration() # Configure camera for video
picam2.configure(video_config)
encoder = H264Encoder()
output = FileOutput("video.h264")
picam2.start()
print("Starting recording...")
picam2.start_recording(encoder, output)
sleep(5)
picam2.stop_recording()
picam2.stop()
print("Recording completed.")