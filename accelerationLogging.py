import time
import os
import board
import digitalio
import adafruit_adxl34x
from adafruit_adxl34x import Range
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.range = Range.RANGE_4_G

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

def setupDisplay():
    global draw
    global backlight
    global font
    global disp
    global top
    global bottom
    global x
    global width
    global height
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = None
    BAUDRATE = 64000000
    spi = board.SPI()
    disp = st7789.ST7789(
        spi,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
        width=240,
        height=240,
        x_offset=0,
        y_offset=80,
    )
    height = disp.width  
    width = disp.height
    image = Image.new("RGB", (width, height))
    rotation = 180
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image, rotation)
    padding = -2
    top = padding
    bottom = height - padding
    x = 0
    font = ImageFont.truetype("DejaVuSans.ttf", 24)
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

setupDisplay()

def showCreatingNewLog():
    text = "Starting New Log"
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    y = top
    draw.text((x, y), text, font=font, fill="#FFFFFF")
    time.sleep(5)



print('creating file')
fileName = createLogFile()
file = open(fileName, 'a')
file.write('time,x,y,z\n')
file.close()

Backlight = digitalio.DigitalInOut(board.D22)
Backlight.switch_to_output()
Backlight.value = True
buttonStartNewLog = digitalio.DigitalInOut(board.D23)
buttonToggleBacklight = digitalio.DigitalInOut(board.D24)
buttonStartNewLog.switch_to_input()
buttonToggleBacklight.switch_to_input()


start = time.monotonic()
print(f'Start Time: {start}\n')
while True:

    if not buttonToggleBacklight.value and Backlight.value == True:
        Backlight.value = False  # turn off backlight
        time.sleep(0.5)
    elif not buttonToggleBacklight.value and Backlight.value == False:
        Backlight.value = True  # turn on backlight
        time.sleep(0.5)

    if buttonToggleBacklight and not buttonStartNewLog.value:  # just button A pressed
        showCreatingNewLog()
        fileName = createLogFile()
        file = open(fileName, 'a')
        file.write('time,x,y,z\n')
        file.close()


    timestamp = time.monotonic()
    accelerationX = accelerometer.acceleration[0]
    accelerationY = accelerometer.acceleration[1]
    accelerationZ = accelerometer.acceleration[2]
    print(f'{timestamp},{accelerationX},{accelerationY},{accelerationZ}\n')

    with open(fileName, 'a') as file:
        print("Writing to file")
        file.write(f'{timestamp},{accelerationX},{accelerationY},{accelerationZ}\n')

    time.sleep(0.2)

 
