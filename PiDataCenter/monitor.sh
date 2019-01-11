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
source /home/pi/.cluster

if [ "$(hostname -s)" == "bitscope_pi3" ]
then
    echo "This is a bitscope pi"
else
    apt-get install python3-pip
    pip3 install requests
    pip3 install python-dateutil
    apt-get install python3-dateutil -y
fi

echo "Running monitor.py with RPI_CLUSTER=$RPI_CLUSTER"
python3 monitor.py
