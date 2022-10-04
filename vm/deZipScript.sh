#!/bin/bash

echo "Lancement du script"

apt-get update # verification des update
apt-get install git -y
apt-get install python3 -y
apt-get install python3-pip -y 
apt-get install cron -y
git clone lien ~/ScriptingSystem # recuperation du projet github

#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "*/1 * * * * ~/ScriptingSystem" >> mycron
#install new cron file
crontab mycron

echo "Fin du script"
rm mycron
