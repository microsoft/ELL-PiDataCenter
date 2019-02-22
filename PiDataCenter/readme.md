## README

This folder contains is the client code for talking to the [ELL PiClusterService](https://github.com/Microsoft/ELL-PiClusterService) that you have
hosted in Azure.  The service code is implemented in Node.js and lives in it's own repo.

## Adding a Raspberry Pi

To add a new Raspberry Pi to the service, first you need to clone the following code into the /home/pi folder of each Raspberry Pi machine:
```shell
cd ~
git clone https://github.com/Microsoft/ELL-PiDataCenter.git
```

And create a file in /home/pi called `.cluster` that contains the following:
```shell
export RPI_CLUSTER="<your_cluster_service_url>"
export RPI_APIKEY="<your_api_key>"
export RPI_PASSWORD="<your_pi_machine_password>"
```

Copy value of these variables from the setup you created when you
followed the directions at [ELL PiClusterService](https://github.com/Microsoft/ELL-PiClusterService).

Then edit the `/etc/rc.local` file on each Raspberry Pi machine to add the following before the bottom `exit` line:
```shell
/home/pi/ELL-PiDataCenter/PiDataCenter/launch.sh
```

Now when you reboot the Raspberry Pi it will automatically connect to the service and you should see the machine listed there.

## Using the Service

In order to use the following scripts, you must also set the same environment variables on whatever machine you are using:

| Varaible       | Value                                       |
|----------------|---------------------------------------------|
| `RPI_CLUSTER`  | The URL of the cluster                      |
| `RPI_APIKEY`   | The API key to use                          |
| `RPI_PASSWORD` | The login password for the cluster machines |

Once the above environment variables are configured you can test the service manually by running these scripts:
* `list.py` to list all available machines and see their status.
* `lock.py ipaddress` to lock a machine listed as free on the website.
* `unlock.py ipaddress` to unlock the machine when you are finished.

This is handy if you want to login using SSH and do long running work on a given machine, perhaps you need to install some new stuff and so on.

But if you want to automate a short job you can import `picluster.py` into your app and do the following:

```python
import picluster
cluster = picluster.PiBoardTable("<app_name>.azurewebsites.net/api/")
machine = self.cluster.wait_for_free_machine("some descriptive job name")
```
This will wait until a machine becomes available, lock it for your job, then you can do whatever you want to do on the machine using SCP and SSH libraries or whatever.  When the job is finished run this:

```python
cluster.unlock(machine.ip_address)
```

This is picking up your user name as well and it ensures you are the only one that can free this machine that you locked.
It is convenient to see who has locked the machine anyway, in case we need to follow up with that person to see if they are done
in the event that something goes wrong and they accidentally forgot to free the machine.

## Example Usage

The [pitest](https://github.com/Microsoft/ELL/tree/master/tools/utilities/pitest) folder in the ELL repo shows how to create a fully automated test that uses this cluster service to get a free raspberry pi, then use SSH and SCP to copy bits over to that machine and run tests on it, get the results back, then unlock the machine.

