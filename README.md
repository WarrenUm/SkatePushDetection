# SkatePushDetection
Used accelerometer to detect and count pushes on a longboard

# Instructions
    - Pi Zero W or Zero 2W
    - PiSugar3
    - SD Card
    - ADXL345 Accelerometer

## Software Setup
Image the SD card with Raspberry PI OS Lite (32-bit) with no desktop environment. I used Raspberry Pi Imager to setup WiFi and ssh. 
Boot up the Pi and ssh to it using:
```ssh user@ip```
and enter your password to continue.
Create a python virtual environment:
```python3 -m venv .env``` and wait for it to finish
Activate the environment:
```source .env/bin/activate```
Install Adafruit-Blinka and adafruit-circuitpython-adxl345x:
```pip3 install Adafruit-Blinka```
```pip3 install adafruit-circuitpython-adxl34x```

Edit .bashrc and add:
```
function cd() {
  builtin cd "$@"

  if [[ -z "$VIRTUAL_ENV" ]] ; then
    ## If env folder is found then activate the vitualenv
      if [[ -d ./.env ]] ; then
        source ./.env/bin/activate
      fi
  else
    ## check the current folder belong to earlier VIRTUAL_ENV folder
    # if yes then do nothing
    # else deactivate
      parentdir="$(dirname "$VIRTUAL_ENV")"
      if [[ "$PWD"/ != "$parentdir"/* ]] ; then
        deactivate
      fi
  fi
}
```
This will activate the venv when moving to the skate directory

Next, make sure that I2C is enabled by running:
```sudo raspi-config nonint do_i2c 0```

Use ```bluetoothctl``` and ```set system-alias``` to skate
```power on
agent on
advertise on
pairable on
pair <phone MAC address>
#complete pass key check
trust <phone MAC address>
devices to check connection
```

Open termius and setup ssh profile with skate.local and the user and pass for the device
#d to skate and activate .env again
```python test.py```

Make a scripts directory for the auto run scripts
```mkdir -p ~/scripts
nano ~/scripts/autopair
```
```#!/bin/bash
bluetoothctl << EOF
connect [enter your MAC add]
EOF
```

Save the file and make it executable with:
```chmod +X ~/scripts/autopair```

Add this service file:
```[Unit]
Description=Auto pairs with phone bluetooth on boot
After=multi-user.target
Requires=bluetooth.target
[Service]
Type=oneshot
User=skate
ExecStart=/usr/bin/bash /home/skate/scripts/autopair
RemainAfterExit=yes
Restart=on-failure
RestartSec=5
[Install]
WantedBy=multi-user.target
```
reload systemctl and enable the service with:
```sudo systemctl daemon-reload
sudo systemctl enable autoupdate
```

Make an updateSkate file:
nano scripts/updateSkate. Paste the following into nano when it opens:
```#!/bin/bash
cd  ~/SkatePushDetection
git pull
```
Hit CTRL+X and Y to save and exit.
Make the file executable with:
```sudo chmod +x /scripts/updateSkate```

### Systemd
Setup systemd to handle autostart scripts
create a systemd service with:
```sudo nano /etc/systemd/system/autoupdate.service```
Copy this service code into nano:
```[Unit]
Description=Pulls Changes from GitHub
After=multi-user.target
Requires=network.target
[Service]
Type=oneshot
User=skate
ExecStart=/usr/bin/bash /home/skate/scripts/updateSkate
Restart=on-failure
RestartSec=5
[Install]
WantedBy=multi-user.target
```
Hit CTRL+X and Y to save and exit.
change the permissions with:
```sudo chmod 644 /etc/systemd/system/autoupdate.service```

reload systemctl and enable the service with:
```sudo systemctl daemon-reload
sudo systemctl enable autoupdate
```
Then reboot the Pi
Check the status of the service with:
```sudo systemctl status autoupdate.service```

The Pi should pull code changes on reboot. If it does not, check the service status for log messages.

Make a new script file to start the logging script when the pi boots:
```cd  ~/SkatePushDetection
source ./.env/bin/activate
python accelerationLogging.py```

Add a new service file to start this script too:
```[Unit]
Description=autoruns logging script
After=multi-user.target
[Service]
Type=oneshot
User=skate
ExecStart=/usr/bin/bash /home/skate/scripts/startLog
Restart=on-failure
RestartSec=5
[Install]
WantedBy=multi-user.target```

```sudo systemctl enable startLog```


#secure copy from pi scp skate@<ip>:~/SkatePushDetection/skateLog_0.csv .
#custom button function to start logging script
#custom buttom function long press to safe shutdown
#script to on boot git pull latest code from github

pip3 install adafruit-circuitpython-gps