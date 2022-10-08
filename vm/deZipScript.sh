#!/bin/bash

echo "Launching the script"

apt-get update  
apt-get install git -y
apt-get install python3 -y
apt-get install python3-pip -y 
pip install paramiko
apt-get install cron -y
git clone https://github.com/Tairox/DezipProject ~/ScriptingSystem

# Copy the content of current crontab file to another temporary file mycron
crontab -l > mycron
# Add new cronjob to the temporary file
echo "0 8 * * * python3 ~/ScriptingSystem/deZipFromWeb.py" >> mycron
# We copy the temporary file back to crontab
crontab mycron

echo "End of the script"
# Deletion of the temporary file
rm mycron
