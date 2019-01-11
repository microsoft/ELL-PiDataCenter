#!/bin/bash

# This script launches the monitor.sh script, after first syncing the latest bits from github.

# first wait for network connection to finish setting up so we can reach github.
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
cd /home/pi/ELL-PiDataCenter/PiDataCenter
git pull
./monitor.sh > /home/pi/monitor.log 2>&1 &
