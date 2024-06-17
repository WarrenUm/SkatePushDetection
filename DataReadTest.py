

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

    