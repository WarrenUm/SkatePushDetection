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
import threading


i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.range = Range.RANGE_16_G

gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,200")

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

def startScreen():
    y = clearDisplay()
    text = 'Go Skate!!\n'
    y = drawText(text,y)
    if gps.has_fix:
        text = "GPS Acquired :)"
        y = drawText(text,y)
    time.sleep(5)
    y = clearDisplay()
    
startScreenThread = threading.Thread(target=startScreen)
startScreenThread.start()


Backlight = digitalio.DigitalInOut(board.D22)
Backlight.switch_to_output()
Backlight.value = True
buttonStartNewLog = digitalio.DigitalInOut(board.D23)
buttonToggleBacklight = digitalio.DigitalInOut(board.D24)
buttonStartNewLog.switch_to_input()
buttonToggleBacklight.switch_to_input()

class DataLogger:
    def __init__(self,gps,acc):
        self._running = True
        self._gps = gps
        self._acc = acc

        fileCount = 0
        fileName = f'skateLog_{fileCount}.csv'
        logFileExists = os.path.isfile(fileName)
        while logFileExists:
            fileCount+=1
            fileName = f'skateLog_{fileCount}.csv'
            logFileExists = os.path.isfile(fileName)
        self._fileName = fileName
        self.displayScreen(self._fileName)
        print('Creating Log File')
        file = open(self._fileName, 'a')
        file.write('time,x,y,z,gpsQuality,gpsTime,gpsAltitude,gpsMPH,gpsLat,gpsLong\n')
        file.close()

    def displayScreen(self,text):
        y = clearDisplay()
        y = drawText(text,y)
        if gps.has_fix:
            text = "GPS Acquired :)"
            y = drawText(text,y)
        time.sleep(5)
        y = clearDisplay()

    def kill(self):
        self._running = False
        
    def logData(self):
        while self._running:
            timestamp = time.monotonic()
            if self._gps.update():
                gpsQuality = self._gps.fix_quality
                gpsTime = self._gps.timestamp_utc
                gpsAltitude = self._gps.altitude_m
                gpsMPH = self._gps.speed_knots
                gpsLat = self._gps.latitude
                gpsLong = self._gps.longitude
            else:
                gpsQuality = None
                gpsTime = None
                gpsAltitude = None
                gpsMPH = None
                gpsLat = None
                gpsLong = None
            accelerationX = self._acc.acceleration[0]
            accelerationY = self._acc.acceleration[1]
            accelerationZ = self._acc.acceleration[2]
            with open(self._fileName, 'a') as file:
                file.write(f'{timestamp},{accelerationX},{accelerationY},{accelerationZ},{gpsQuality},{gpsTime},{gpsAltitude},{gpsMPH},{gpsLat},{gpsLong}\n')

logger = False
while True:

    if not buttonToggleBacklight.value and Backlight.value == True:
        Backlight.value = False  # turn off backlight
        time.sleep(0.1)
    elif not buttonToggleBacklight.value and Backlight.value == False:
        Backlight.value = True  # turn on backlight
        time.sleep(0.1)

    if buttonToggleBacklight and not buttonStartNewLog.value:  # just button A pressed
        print("Button A Pressed")
        if logger:
            print("Killing logData thread")
            logger.kill()
            thr.join()
            print("Thread Joined")
        print("Creating new DataLogger")
        logger = DataLogger(gps,accelerometer)
        print("Creating new thread")
        thr = threading.Thread(target=logger.logData)
        print("Starting thread")
        thr.start()

    time.sleep(0.15)

 