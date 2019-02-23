#!/usr/bin/env python3
###################################################################################################
#
#  Project: Embedded Learning Library (ELL)
#  File: remote.py
#  Authors: Chris Lovett
#
#  Requires: Python 3.x
#
###################################################################################################
import argparse
import logging
import re
import sys

import endpoint

from dask import compute, delayed
import dask.multiprocessing

import picluster
import remoterunner


class RemoteHelper:
    def __init__(self):
        self.cluster_address = endpoint.url
        self.cluster = picluster.PiBoardTable(self.cluster_address, endpoint.apikey)
        self.lock_override = False
        self.locked_ip = None

    def __enter__(self):
        """Called when this object is instantiated with 'with'"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Called on cleanup of this object that was instantiated with 'with'"""
        # cleanup locked machines if ctrl+c is used to interrupt this script.
        if self.locked_ip:
            self.cluster.unlock(self.locked_ip)

    def run_remote(self, ip, command, copyfiles, target_dir, password, verbose=False):
        self.lock_override
        machine = None
        result = "=========={}====================================\n".format(ip)

        if not lock_override:
            try:
                machine = self.cluster.get(ip)
                if machine.current_user_name or machine.command == "Lock":
                    result += "Skipping machine {} because it is locked by {}".format(ip, machine.current_user_name)
                    return result
                machine = self.cluster.lock(ip, "remote exec")
                self.locked_ip = ip
            except:
                errorType, value, traceback = sys.exc_info()
                print(ip + ": ### lock failed: " + str(value))
                return result

        runner = remoterunner.RemoteRunner(cluster=self.cluster_address, source_files=copyfiles,
                                           ipaddress=ip, username="pi", password=password,
                                           target_dir=target_dir, verbose=verbose)

        try:
            runner.connect_ssh()
            if copyfiles:
                runner.publish_bits()
            output = runner.exec_remote_command(command)
            result += "\n".join(output)
        except:
            errorType, value, traceback = sys.exc_info()
            print(ip + ": ### connection failed: " + str(value))

        if not lock_override:
            try:
                machine = self.cluster.get(ip)
                if machine.current_user_name != "" or machine.command != "Free":
                    self.cluster.unlock(ip)
                self.locked_ip = None
            except:
                errorType, value, traceback = sys.exc_info()
                print(ip + ": ### unlock failed: " + str(value))

        return result

    def get_matching_machines(self, selected_ips, platform, ignore_dead_status=False):
        addresses = []
        for e in self.cluster.get_all():
            if ignore_dead_status or e.alive:
                for s in selected_ips:
                    if s == '*' or s == e.ip_address or re.match(s, e.ip_address):
                        if platform is None or platform in e.platform:
                            if e.ip_address not in addresses:
                                addresses += [e.ip_address]
        return addresses


if __name__ == '__main__':
    cmd = []
    addresses = []

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser("""Run a command on every available raspberry pi
    e.g.
        python remote.py -c cat /proc/cpuinfo -a 157.54.158.128 157.54.158.36
        python remote.py -c cat /proc/cpuinfo -a *
    """)
    parser.add_argument("--script", "-s", nargs="+", help="A script file to copy to the machine before running --command")
    parser.add_argument("--target_dir", "-t", nargs="+", help="Location to copy --scripts on target machine (default /home/pi)", default="/home/pi")    
    parser.add_argument("--command", "-c", nargs="+", help="The command line arguments to run on the remote machines")
    parser.add_argument("--addresses", "-a", nargs="*", help="The remote addresses to use (default *)", default="*")
    parser.add_argument("--max_threads", "-m", type=int, help="Maximum number of parallel jobs (default 8)", default=8)
    parser.add_argument("--lock_override", "-o",
                        help="Override locked status and execute command anyway (default False)",
                        action="store_true")
    parser.add_argument("--dead_override", "-do",
                        help="Override dead status and execute command anyway (default False)",
                        action="store_true")
    parser.add_argument("--verbose", "-v", help="Print output incrementally (default False)", action="store_true")
    parser.add_argument("--platform", "-p", help="An optional sub-string to match with the target pi (default None)")
    args = parser.parse_args()

    cmd = args.command
    lock_override = args.lock_override
    verbose = args.verbose
    target_dir = args.target_dir
    copyfiles = args.script

    with RemoteHelper() as helper:
        addresses = helper.get_matching_machines(args.addresses, args.platform, args.dead_override)
        if len(addresses) == 0:
            print("No machines found macthing {}".format(args.addresses))

        cmd = " ".join(cmd)
        results = []
        if args.max_threads == 1:
            for ip in addresses:
                results += [helper.run_remote(ip, cmd, copyfiles, target_dir, endpoint.password, verbose)]
        else:
            values = [delayed(helper.run_remote)(ip, cmd, copyfiles, target_dir, endpoint.password, verbose) for ip in addresses]
            results = compute(*values, get=dask.multiprocessing.get, num_workers=args.max_threads)

        if not verbose:
            print("\n".join(results))
