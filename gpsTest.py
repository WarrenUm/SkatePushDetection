import time
import os
import board
import adafruit_gps


i2cgps = board.I2C()  # For using the built-in STEMMA QT connector on a microcontroller
gps = adafruit_gps.GPS_GtopI2C(i2cgps)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b"PMTK220,1000")

while True:
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