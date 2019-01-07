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
    sudo cp config.txt /boot/config.txt
    echo "config has changed, pi needs a reboot" > reboot.txt
elif [ -f reboot.txt ]; then
    rm reboot.txt
fi

source /home/pi/.bashrc

if [[ -d "/home/pi/miniconda3" ]]; then
    source activate py34
    pip install requests
    pip install python-dateutil
else
    sudo pip3 install requests
    sudo pip3 install python-dateutil
    sudo apt-get install python3-dateutil -y
fi

echo "running monitor.py..."
sudo python3 monitor.py

