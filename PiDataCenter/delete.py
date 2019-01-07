#!/usr/bin/env python3
###################################################################################################
##
##  Project:  Embedded Learning Library (ELL)
##  File:     delete.py
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
  parser = argparse.ArgumentParser("""Delete a given raspberry pi machine from the list
  e.g.
      python delete.py 157.54.158.128
  """
  )
  parser.add_argument("ip_addresses", nargs="*", help="One or more addresses of the machines to delete")
  args = parser.parse_args()
  
  
  cluster = picluster.PiBoardTable(endpoint.url, endpoint.apikey)
  machines = cluster.get_matching_machines(args.ip_addresses)
  machines.sort(key=lambda x: x.ip_address)
  if len(machines) == 0:
      print("no machines maching %s" % (args.ip_addresses))

  for r in machines:
    if r.command == 'Lock':
      print("machine is locked!")
    else:
      try:
        print("Deleting machine {}...".format(r.ip_address), end='')
        s = cluster.delete(r.ip_address)        
        print("machine is deleted!")
      except:
        errorType, value, traceback = sys.exc_info()
        print("### Exception: " + str(errorType) + ": " + str(value))
  
if __name__ == '__main__':
  main()
