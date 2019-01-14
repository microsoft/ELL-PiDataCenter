#!/usr/bin/env python3
###################################################################################################
#
#  Project:  Embedded Learning Library (ELL)
#  File:     list.py
#  Authors:  Chris Lovett
#
#  Requires: Python 3.x
#
###################################################################################################
import argparse

import picluster
import endpoint


def main():
  parser = argparse.ArgumentParser("""List all or some subset of pi machines
  e.g.
      python list.py
      python list.py 10.*
      python list.py --me
  """
                                   )
  parser.add_argument("ip_addresses", nargs="*", help="The address of the machine(s) to list")
  args = parser.parse_args()

  cluster = picluster.PiBoardTable(endpoint.url, endpoint.apikey)

  machines = cluster.get_matching_machines(args.ip_addresses)
  machines.sort(key=lambda x: x.ip_address)

  for e in machines:
    msg = e.ip_address
    if e.hostname:
      msg += " " + e.hostname
    if e.command == "Lock":
      msg += " locked"
    if e.current_user_name:
      msg += " by " + e.current_user_name
    if e.current_task_name:
      msg += " for '" + e.current_task_name + "'"
    if not e.alive:
      msg += " is dead?"

    print(msg)


if __name__ == '__main__':
  main()
