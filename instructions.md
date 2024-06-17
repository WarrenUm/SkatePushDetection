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

#setup systemd to handle autostart scripts
create a systemd service with sudo nano /etc/systemd/system/autoupdate.service

change permissions sudo chmod 644 /etc/systemd/system/name-of-your-service.service
reload systemctl and enable the service
sudo systemctl daemon-reload
sudo systemctl enable name-of-your-service.service
Then reboot
Check status with sudo systemctl status autoupdate.service

```[Unit]
Description=auto updates skate scripts from GitHub
After=multi-user.target
Requires=network.target
[Service]
Type=idle
User=skate
ExecStart=/usr/bin/bash /home/skate/scripts/updateSkate
[Install]
WantedBy=multi-user.target
```



#secure copy from pi scp skate@<ip>:~/skate/skateLog_0.csv .
#custom button function to start logging script
#custom buttom function long press to safe shutdown
#script to on boot git pull latest code from github