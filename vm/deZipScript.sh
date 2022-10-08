#!/bin/bash

echo "Launching the script"

# Check if the script is run as root
if [ "$EUID" -ne 0 ];then
    echo "Please run this script as root"
    exit 1
fi

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

# Deletion of the temporary file
rm mycron

echo "End of the script"
