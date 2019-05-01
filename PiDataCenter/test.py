#!/usr/bin/env python3
###################################################################################################
#
#  Project: Embedded Learning Library (ELL)
#  File: test.py
#  Authors: Chris Lovett
#
#  Requires: Python 3.x
#
###################################################################################################
import argparse
import picluster

# This test script shows how to interact with the Azure pi data center cloud
# service.
# It uses the 'requests' module to do HTTP interactions with Json data.
# See http://docs.python-requests.org/en/v1.0.0/user/quickstart/
import endpoint

import dask.bag

ip = "192.168.1.999"  # make it invalid ip address on purpose so it never colides with real machine
entity = {
    'IpAddress': ip,
    'OsName': 'Raspbian',
    'OsVersion': 'Jesse',
    'CurrentTaskName': "RollingBuild",
    'CurrentUserName': '',
    'Command': ''
}
user = "Test"


def test_assert(e, message):
    status = "SUCCESS"
    if not e:
        status = "FAILED"
    print("{}, {}".format(message, status))


def get_free_machine(cluster, id):
    return cluster.wait_for_free_machine("test_" + str(id), ignore_alive=True)


def test(server):
    # test api key security
    try:
        t = picluster.PiBoardTable(server, "123", user)
        a = picluster.PiBoardEntity(entity)
        r = t.update(a)
        test_assert(False, "api key security is working")
    except Exception as e:
        test_assert(str(e) == "api key mismatch", "api key security is working")

    # add or update
    t = picluster.PiBoardTable(server, endpoint.apikey, user)

    # insert our test entity so we can play with it.
    a = picluster.PiBoardEntity(entity)
    r = t.update(a)
    test_assert(r.ip_address == ip, "add or update entity")

    # get all
    r = t.get_all()
    test_assert(len(r) > 0 and ip in [x.ip_address for x in r], "get_all")

    # get the entity we added
    r = t.get(ip)
    test_assert(r and r.ip_address == ip, "get the entity we added")

    # locking
    r = t.lock(ip, 'Test')
    test_assert(r and r.ip_address == ip and r.current_user_name == t.username, "lock our machine")

    # now try and free the device using wrong user name
    saved = t.username
    t.username = 'Chuck'
    failed = False
    try:
        r = t.unlock(ip)
        failed = False
    except:
        failed = True
    t.username = saved
    test_assert(failed, "try and free the device using wrong user name")

    # double check this is really the case
    r = t.get(ip)
    test_assert(r and r.ip_address == ip, "ensure entity is still there")

    # now try and free the device using correct user name
    r = t.unlock(ip)
    test_assert(r and r.ip_address == ip, "unlock our machine")

    # check it really is not locked
    r = t.get(ip)
    test_assert(r and r.current_user_name != t.username, "lock is gone")

    # delete
    r = t.delete(ip)
    test_assert(r and r.current_user_name != t.username, "delete our machine")

    # create 10 machines so we can lock them all in parallel
    for i in range(10):
        a.ip_address = "255.255.255.{}".format(i)
        r = t.update(a)

    # now a multithreaded lock to make sure it is safe!
    dask.config.set(scheduler='threads')
    jobs = dask.bag.from_sequence(list(range(10)))
    results = dask.bag.map(lambda id: get_free_machine(t, id), jobs).compute()

    test_assert(len(results) == 10, "We have locked 10 machines in parallel")

    addresses = [r.ip_address for r in results]
    unique_list = set(addresses)
    test_assert(len(addresses) == len(unique_list), "locked machines are unique")

    for m in unique_list:
        if len([x for x in addresses if x == m]) > 1:
            print("Machine {} locked twice, which should not be possible!!".format(m))
        t.unlock(m)
        t.delete(m)


if __name__ == '__main__':

    parser = argparse.ArgumentParser("Test the picluster service")
    parser.add_argument("url", help="optional url to override the default so you can test locally, like 'http://localhost:1337/'", default=endpoint.url)
    args = parser.parse_args()

    test(args.url)
