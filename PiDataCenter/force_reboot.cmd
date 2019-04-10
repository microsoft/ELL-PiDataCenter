REM use this script to reboot all registered devices even if they are currently locked.
python remote.py -c "echo rebooting... && sudo reboot" -a * --lock_override  
