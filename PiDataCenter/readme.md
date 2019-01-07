
## README

This folder contains is the client code for talking to the Azure Web Service that maintains our 
Raspberry Pi list of available machines.  The service code is implemented in Node.js and lives in it's own repo.

## Adding a Raspberry Pi

To add a Raspberry Pi to the service simply edit the `/etc/rc.local` file and add the following before the bottom `exit` line:
```shell
/home/pi/ELL-PiDataCenter/PiDataCenter/monitor.sh&
```
Don't forget the ampersand.  

Then run the following from the /home/pi folder:
```shell
cd ~
git clone https://github.com/Microsoft/ELL-PiDataCenter.git
pushd ELL-PiDataCenter/PiDataCenter
chmod +x monitor.sh
popd
```

Now when you reboot your pi it will automatically connect to the service and you should see the machine listed there.

## Using the Service

The easiest way to use the service is to use `ELL/tools/utilities/pitest/drivetest.py` which is already setup to use this service.

You can also use the service manually by running these two scripts:
* `lock.py ipaddress` to lock a machine listed as free on the website.
* `unlock.py ipaddress` to unlock the machine when you are finished.

This is handy if you want to login using SSH and do long running work on a given machine, perhaps you need to install some new stuff and so on.

But if you want to automate a short job you can import `picluster.py` into your app and do the following:

```python
import picluster
import endpoint
cluster = picluster.PiBoardTable(endpoint.url, endpoint.apikey)
machine = cluster.wait_for_free_machine("some descriptive job name")
```
This will wait until a machine becomes available, lock it for your job, then you can do what drivetest does to send the job to the machine using SCP and SSH libraries.  When the job is finished run this:

```python
cluster.unlock(machine.ip_address)
```

This is picking up your user name as well and it ensures you are the only one that can free this machine that you locked.
It is convenient to see who has locked the machine anyway, in case we need to follow up with that person to see if they are done
in the event that something goes wrong and they accidentally forgot to free the machine.

