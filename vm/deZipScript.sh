#!/bin/bash

echo "Lancement du script"

apt-get update  
apt-get install git -y
apt-get install python3 -y
apt-get install python3-pip -y 
pip install paramiko
apt-get install cron -y
git clone https://github.com/Tairox/DezipProject ~/ScriptingSystem

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "* * * * * python3 ~/ScriptingSystem/deZipFromWeb.py" >> mycron
#install new cron file
crontab mycron

echo "Fin du script"
rm mycron
