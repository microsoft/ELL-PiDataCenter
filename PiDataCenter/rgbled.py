#!/usr/bin/env python3
###################################################################################################
#
#  Project: Embedded Learning Library (ELL)
#  File: rgbled.py
#  Authors: Chris Lovett
#
#  Requires: Python 3.x
#
###################################################################################################
import sys
import time


try:
    import RPi.GPIO as GPIO
except:
    print("this needs to run as admin")
    sys.exit(1)


# This code is for the anode style RGB LED
# where the long pin is connected to 3.3 V
# and a HIGH GPIO output turns off that color
# and LOW GPIO output causes 3.3V to flow (so color is on)
RED_PIN = 19
GREEN_PIN = 15
BLUE_PIN = 13


class LedPwmDriver:

    def __init__(self):
        self.chan_list = [RED_PIN, GREEN_PIN, BLUE_PIN]
        self.red = 0  # off
        self.green = 0
        self.blue = 0
        self.off = True
        self.setup()

    def setup(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.chan_list, GPIO.OUT, initial=GPIO.HIGH)
        self.red_pwm = GPIO.PWM(RED_PIN, 100)
        self.green_pwm = GPIO.PWM(GREEN_PIN, 100)
        self.blue_pwm = GPIO.PWM(BLUE_PIN, 100)

    def set_color(self, r, g, b):
        # convert rgb to pwm count
        self.red = self.limit(r)
        self.green = self.limit(g)
        self.blue = self.limit(b)
        self.red_pwm.start(100 - self.red)
        self.green_pwm.start(100 - self.green)
        self.blue_pwm.start(100 - self.blue)

    def limit(self, c):
        if c < 0:
            c = 0
        if c > 100:
            c = 100
        return c

    def stop(self):
        self.red_pwm.stop()
        self.green_pwm.stop()
        self.blue_pwm.stop()
        time.sleep(1)
        GPIO.output(self.chan_list, GPIO.HIGH)

    def fade_to(self, r, g, b, seconds):
        rate = 1000.0 / 60.0  # 60 FPS should be good
        steps = float(seconds) * rate
        cr = self.red
        cg = self.green
        cb = self.blue
        for i in range(int(steps)):
            led.set_color(((r * i) + (steps - i) * cr) / steps,
                          ((g * i) + (steps - i) * cg) / steps,
                          ((b * i) + (steps - i) * cb) / steps)
            time.sleep(rate / 1000.0)
        self.set_color(r, g, b)


if __name__ == '__main__':
    delay = 0.3
    led = LedPwmDriver()

    fade_time = 2  # second
    max = 100
    led.fade_to(max, 0, 0, fade_time)
    led.fade_to(0, 0, 0, fade_time)
    led.fade_to(0, max, 0, fade_time)
    led.fade_to(0, 0, 0, fade_time)
    led.fade_to(0, 0, max, fade_time)
    led.fade_to(0, 0, 0, fade_time)

    led.fade_to(max, max, 0, fade_time)
    led.fade_to(0, 0, 0, fade_time)
    led.fade_to(max, 0, max, fade_time)
    led.fade_to(0, 0, 0, fade_time)
    led.fade_to(0, max, max, fade_time)
    led.fade_to(0, 0, 0, fade_time)

    led.fade_to(max, max, max, fade_time)
    led.fade_to(0, 0, 0, fade_time)

    led.stop()
