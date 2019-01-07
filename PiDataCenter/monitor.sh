#!/bin/bash

# To install this script so it executes on boot simply add this line to your /etc/rc.local
# /home/pi/monitor.sh&
# And add it just before the final "exit 0" line.  Don't forget the ampersand.

cd /home/pi/

while :
do
    FOUND="$(ping -c 2 github.com | sed ':a;N;$!ba;s/.*bytes from.*/FOUND/g' )"
    if [[ "$FOUND" == "FOUND" ]]
    then
        break
    fi
    echo "Not finding 'github.com', sleeping for 5 seconds..."
    sleep 5
done

echo Updating scripts from 'github.com'...

fetch() {
    local file=$1
    local url=$2
    echo "downloading: $url"
    wget -q -O $file $url
    while [ $? -ne 0 ]
    do
       echo "### error: download $url failed, trying again in a second"
       sleep 1      
       wget -q -O $file $url 
    done
}

pushd /home/pi/ELL-PiDataCenter/PiDataCenter
chmod +x setup.sh
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

if [[ -d "/home/pi/miniconda3" ]]; then
    export PATH="/home/pi/miniconda3/bin:$PATH"
    pip install requests
    pip install python-dateutil
else
    sudo pip3 install requests
    sudo pip3 install python-dateutil
    sudo apt-get install python3-dateutil -y
fi

echo "running monitor.py..."
sudo python3 monitor.py
