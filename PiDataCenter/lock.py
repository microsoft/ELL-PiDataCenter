#!/usr/bin/env python3
###################################################################################################
##
##  Project:  Embedded Learning Library (ELL)
##  File:     lock.py
##  Authors:  Chris Lovett
##
##  Requires: Python 3.x
##
###################################################################################################
import argparse
import socket
import time
import picluster
import platform
import sys

import endpoint

def main():
  parser = argparse.ArgumentParser("""Lock a given raspberry pi machine
  e.g.
      python lock.py 157.54.158.128 "perf experiments"
  """
  )
  parser.add_argument("ip_addresses", nargs="+", help="The address of the machine(s) to lock")
  parser.add_argument("--reason", "-r", help="reason to show in the current_task_name field")
  args = parser.parse_args()

  reason = "Manual"
  if args.reason:
      reason = args.reason

  cluster = picluster.PiBoardTable(endpoint.url, endpoint.apikey)

  machines = cluster.get_matching_machines(args.ip_addresses)
  for r in machines:
    ip = r.ip_address
    if r.command == 'Lock':
      print("machine is already locked by someone else!")
    else:
      try:
        s = cluster.lock(ip, reason)        
        print("machine %s is now locked by you!" % (ip))
      except:
        errorType, value, traceback = sys.exc_info()
        print("### Exception locking machine {}: {}: {}".format(ip, errorType, value))          

if __name__ == '__main__':
  main()
