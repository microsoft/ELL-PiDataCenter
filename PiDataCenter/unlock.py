#!/usr/bin/env python3
###################################################################################################
##
##  Project:  Embedded Learning Library (ELL)
##  File:     unlock.py
##  Authors:  Chris Lovett
##
##  Requires: Python 3.x
##
###################################################################################################
import socket
import time
import picluster
import platform
import sys
import argparse
import endpoint 

def main():
  parser = argparse.ArgumentParser("""Unlock a given raspberry pi machine
  e.g.
      python unlock.py 157.54.158.128
      python unlock.py 157.*
      python unlock.py --me
  """
  )
  parser.add_argument("ip_addresses", nargs="*", help="The address of the machine(s) to unlock")
  parser.add_argument("--me", help="unlock all machines locked by me",  action="store_true", default=False)
  parser.add_argument("--lock_override", help="unlock even if it was locked by someone else",  action="store_true", default=False)
  args = parser.parse_args()
  cluster = picluster.PiBoardTable(endpoint.url, endpoint.apikey)
  machines = cluster.get_matching_machines(args.ip_addresses)
  count = 0
  if args.me:
    for e in machines:
      if e.current_user_name == cluster.username and e.command == 'Lock':
          print("unlocking " + e.ip_address)
          cluster.unlock(e.ip_address)
  else:
    for e in machines:
      if e.command == 'Lock':
        count += 1
        if e.current_user_name != cluster.username:
          if not args.lock_override:
            print("machine {} was locked by {}, please talk first!".format(e.ip_address, e.current_user_name))
            continue
          else:
            print("overriding lock on machine {}".format(e.ip_address))
            saved = cluster.username
            cluster.username = e.current_user_name
            try:
              cluster.unlock(e.ip_address)
            except:  
              errorType, value, traceback = sys.exc_info()
              print("### Exception locking machine {}: {}: {}".format(e.ip_address, errorType, value))
            cluster.username = saved
        else:
          print("unlocking " + e.ip_address)
          cluster.unlock(e.ip_address)
    if count == 0:
      print("no machines matching your input were locked")

if __name__ == '__main__':
  main()
