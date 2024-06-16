import time
import os
import board
import adafruit_adxl34x

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

fileCount=0
def createLogFile(fileCount=0):
    fileName = f'skateLog_{fileCount}.csv'
    logFileExists = os.path.isfile(fileName)
    while logFileExists:
        print(f'file exists {fileCount}')
        fileCount+=1
        fileName = f'skateLog_{fileCount}.csv'
        logFileExists = os.path.isfile(fileName)
    
    print('returning filename')
    return fileName

print('creating file')
fileName = createLogFile()
file = open(fileName, 'a')
file.write('time,x,y,z\n')
file.close()


start = time.monotonic()
print(f'Start Time: {start}\n')
while True:

    timestamp = time.monotonic()
    accelerationX = accelerometer.acceleration[0]
    accelerationY = accelerometer.acceleration[1]
    accelerationZ = accelerometer.acceleration[2]
    print(f'{timestamp},{accelerationX},{accelerationY},{accelerationZ}\n')

    with open(fileName, 'a') as file:
        print("Writing to file")
        file.write(f'{timestamp},{accelerationX},{accelerationY},{accelerationZ}\n')

    time.sleep(0.2)

 
