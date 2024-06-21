import time
import os
import board
import digitalio
import busio
import adafruit_gps
import adafruit_adxl34x
from adafruit_adxl34x import Range
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789


i2cgps = board.I2C()  # For using the built-in STEMMA QT connector on a microcontroller
gps = adafruit_gps.GPS_GtopI2C(i2cgps)
gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b"PMTK220,1000")

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.range = Range.RANGE_16_G

global draw
global backlight
global font
global disp
global top
global bottom
global x
global width
global height
global image
global rotation
global fileCount

fileCount = 0
def createLogFile(fileCount):
    fileName = f'skateLog_{fileCount}.csv'
    logFileExists = os.path.isfile(fileName)
    while logFileExists:
        fileCount+=1
        fileName = f'skateLog_{fileCount}.csv'
        logFileExists = os.path.isfile(fileName)
    return fileName

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
y = top
font = ImageFont.truetype("DejaVuSans.ttf", 24)
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


def clearDisplay():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    disp.image(image, rotation)
    y = top
    return y

def drawText(text,y):    
    draw.text((x,y),text,font=font,fill=("#FFFFFF"),align="left",)
    y += font.getbbox(text)[3]
    disp.image(image, rotation)
    return y*2

def newLogfile():
    y = clearDisplay()
    fileName = createLogFile(fileCount)
    text = f"New Log File:\n {fileName}"
    y = drawText(text,y)
    file = open(fileName, 'a')
    file.write('time,x,y,z\n')
    file.close()
    text = "Done!"
    y = drawText(text,y)
    y = clearDisplay()


print('Creating Initial File')
fileName = createLogFile(fileCount)
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
while True:

    if not buttonToggleBacklight.value and Backlight.value == True:
        Backlight.value = False  # turn off backlight
        time.sleep(0.1)
    elif not buttonToggleBacklight.value and Backlight.value == False:
        Backlight.value = True  # turn on backlight
        time.sleep(0.1)

    if buttonToggleBacklight and not buttonStartNewLog.value:  # just button A pressed
        print("buttonA Pressed")
        newLogfile()
        
    if gps.has_fix:
        print(
                "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                    gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
                    gps.timestamp_utc.tm_mday,  # struct_time object that holds
                    gps.timestamp_utc.tm_year,  # the fix time.  Note you might
                    gps.timestamp_utc.tm_hour,  # not get all data like year, day,
                    gps.timestamp_utc.tm_min,  # month!
                    gps.timestamp_utc.tm_sec,
                )
            )
    else:
        print("no gps fix")


    timestamp = time.monotonic()
    accelerationX = accelerometer.acceleration[0]
    accelerationY = accelerometer.acceleration[1]
    accelerationZ = accelerometer.acceleration[2]
    print(f'{timestamp},{accelerationX},{accelerationY},{accelerationZ}\n')

    with open(fileName, 'a') as file:
        file.write(f'{timestamp},{accelerationX},{accelerationY},{accelerationZ}\n')

    time.sleep(0.2)

 
