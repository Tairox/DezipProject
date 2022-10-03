#!/bin/bash

echo "Lancement du script"

apt-get update  
apt-get install python3 -y
apt-get install python3-pip -y 
python3 deZipFromWeb.py 

echo "Fin du script"
