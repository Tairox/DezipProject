#!/bin/bash

echo "Launching the script"

sudo apt-get update  
sudo apt-get install git -y
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y 
sudo pip install paramiko
sudo apt-get install cron -y
sudo git clone https://github.com/Tairox/DezipProject ~/ScriptingSystem

# Copy the content of current crontab file to another temporary file mycron
sudo crontab -l > mycron
# Add new cronjob to the temporary file
sudo echo "0 8 * * * python3 ~/ScriptingSystem/deZipFromWeb.py" >> mycron
# We copy the temporary file back to crontab
sudo crontab mycron

echo "End of the script"
# Deletion of the temporary file
sudo rm mycron
