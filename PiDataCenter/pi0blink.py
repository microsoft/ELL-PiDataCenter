#!/usr/bin/python3

import argparse
import time, os
import gpiozero as io

def blink(count):
  led = io.LED(2)

  for i in range(count):
    led.on()
    time.sleep(0.30)
    led.off()
    time.sleep(0.30)

if __name__ == '__main__':
  parser = argparse.ArgumentParser("""Lock a given raspberry pi machine
  e.g.
      python lock.py 157.54.158.128 "perf experiments"
  """
  )
  parser.add_argument("--count", "-c", type=int, help="number of blinks (default 10)", default=10)
  args = parser.parse_args()
  blink(args.count)