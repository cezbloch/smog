# smog
Air Quality Monitor application to monitor PM 2.5 and PM10 from SDL607 device. Easily extendable to handle any other device and push data into any storage. 

---------- create a deamon service launching at system start-up --------------
sudo apt-get install daemontools daemontools-run
- create service named 'smog'
sudo mkdir /etc/service/smog
- make start-up script called 'run'
sudo nano /etc/service/smog/run
- type
#!/bin/bash
cd /home/pi/smog/
exec sudo /usr/bin/python /home/pi/smog/AirMonitorText.py home --silent
- set permissions
sudo chmod u+x /etc/service/smog/run
- check status
sudo svstat /etc/service/smog
- kill
sudo svc -k /etc/service/smog
- start
sudo svc -u /etc/service/smog
