#create skate directory and move to it
#create a python venv - python3 -m venv .env and wait for it to finish
#activate with source .env/bin/activate
#install Adafruit-Blinka with pip3 install Adafruit-Blinka wait for it to install

#make sure that I2C is enabled. Run:
#sudo raspi-config nonint do_i2c 0

#install adafruit-circuitpython-adxl34x
#pip3 install adafruit-circuitpython-adxl34x

#use bluetoothctl and set system-alias to skate
#power on
#agent on
#advertise on
#pairable on
#pair <phone MAC address>
#complete pass key check
#trust <phone MAC address>
#devices to check connection

#open termius and setup ssh profile with skate.local and the user and pass for the device
#cd to skate and activate .env
#python test.py

#make a scripts dir - mkdir -p ~/scripts
#make an autopair script - nano ~/scripts/autopair
#add:
# #!/bin/bash
# bluetoothctl << EOF
# connect [enter your MAC add]
# EOF
#save the file and make it executable with:
# chmod +X ~/scripts/autopair
# make scripts/updateSkate and made executable too
# #!/bin/bash
#cd ~/SkatePushDetection
#git pull
#reboot to test

#secure copy from pi scp skate@<ip>:~/skate/skateLog_0.csv .
#custom button function to start logging script
#custom buttom function long press to safe shutdown
#script to on boot git pull latest code from github

import time
import board
import adafruit_adxl34x

i2c = board.I2C()

accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection(threshold=30)

maxPushAccelerationX = 15
pushCounter = 0
while True:
    eventDetected = accelerometer.events["motion"]
    accelerationX = accelerometer.acceleration[0]
    if eventDetected and accelerationX > 0 and accelerationX < maxPushAccelerationX:
        print(f"Forward Push Detected with Acceleration: {accelerationX}, Incrementing Counter")
        pushCounter+=1
        print(f"Pushes Detected: {pushCounter}")
        time.sleep(0.3)
    if eventDetected and accelerationX > maxPushAccelerationX:
        print(f"Acceleration of: {accelerationX} too High")
        time.sleep(0.3)

    