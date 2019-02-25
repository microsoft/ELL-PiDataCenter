#!/usr/bin/env python3
###################################################################################################
#
#  Project: Embedded Learning Library (ELL)
#  File: monitor.py
#  Authors: Chris Lovett
#
#  Requires: Python 3.x
#
###################################################################################################
import os
import platform
import socket
import subprocess
import sys
import time
import picluster
import endpoint


print("using python version:", platform.python_version())


# This scipt runs on a raspberry pi and it pings the Azure service every 60
# seconds to keep it updated on the pi behavior.
def get_local_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  bing_ip = socket.gethostbyname('www.bing.com')
  s.connect((bing_ip, 80))
  localip, port = s.getsockname()
  s.close()
  return localip


def get_hostname():
    return socket.gethostname()


def get_temperature():
    try:
        tempstring = subprocess.check_output(['cat /sys/class/thermal/thermal_zone0/temp']).decode('utf-8')
        return "{}'C".format(float(tempstring) / 1000)
    except:
        return ''


def get_system_load():
    try:
        return '{} : {} : {}'.format(*os.getloadavg())
    except:
        return ''


# setup loop, waiting for network to be available
while True:
    try:
        cluster = picluster.PiBoardTable(endpoint.url, endpoint.apikey)

        ip = get_local_ip()
        r = cluster.get(ip)
        if r:
            if os.path.isfile("nounlock"):
                print("nounlock override, leaving machine locked")
                os.remove("nounlock")  # one time override of auto-unlock behavior
            elif r.command == 'Lock':
                try:
                    print("machine was locked when we rebooted, so free the lock now!")
                    cluster.username = r.current_user_name
                    cluster.unlock(ip)
                except:
                    errorType, value, traceback = sys.exc_info()
                    print("unlock failed: {}: {}".format(str(errorType), str(value)))
        else:
            r = picluster.PiBoardEntity()

        # setup heartbeat message, which doesn't modify current user or task or
        # command.
        r.ip_address = ip
        r.current_task_name = None
        r.current_user_name = None
        r.command = None
        break

    except:
        errorType, value, traceback = sys.exc_info()
        print("setup error: {}: {}".format(str(errorType), str(value)))
        time.sleep(60)

# heartbeat loop
while True:
    try:
        # re-fetch our local ip in case it changed
        r.ip_address = get_local_ip()
        r.hostname = get_hostname()
        r.temperature = get_temperature()
        r.system_load = get_system_load()
        cluster.update(r)
    except:
        errorType, value, traceback = sys.exc_info()
        msg = "network error: {}:{}, perhaps we don't have an ip address right now " + \
              "so sleep and try again later..."
        print(msg.format(str(errorType), str(value)))

    try:
        now = time.localtime()
        delay = 60 - now.tm_sec
        if delay > 0:
            time.sleep(60 - now.tm_sec)  # try and sync on minutes
    except:
        time.sleep(10)
