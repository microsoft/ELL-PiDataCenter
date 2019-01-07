#!/bin/bash

cd /home/pi/

pushd /home/pi/ELL-PiDataCenter/PiDataCenter
chmod +x monitor.sh

# check whether the config file has changed or not
hash=$(cat /boot/config.txt | sha256sum)
newhash=$(cat config.txt | sha256sum)

echo hash=$hash
echo newhash=$newhash

if [ "$hash" != "$newhash" ]
then
    cp config.txt /boot/config.txt
    echo "config has changed, pi needs a reboot" > reboot.txt
elif [ -f reboot.txt ]; then
    rm reboot.txt
fi

source /home/pi/.bashrc

echo === Checking that RPI_CLUSTER=$RPI_CLUSTER

if [[ -d "/home/pi/miniconda3" ]]; then
    pip install requests
    pip install python-dateutil
else
    pip3 install requests
    pip3 install python-dateutil
    apt-get install python3-dateutil -y
fi

echo "running monitor.py..."
python3 monitor.py
