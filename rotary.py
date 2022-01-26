#!/usr/bin/env python3

from RPi import GPIO
from time import sleep
import subprocess

clk = 22
dt = 27
btn = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clkLastState = GPIO.input(clk)

def swClicked(channel):
        subprocess.call(['amixer', '-q', 'set', 'Attenuation', 'toggle'])

GPIO.add_event_detect(btn, GPIO.FALLING, callback=swClicked, bouncetime=300)

try:
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                subprocess.call(['amixer', '-q', 'set', 'Attenuation', '1dB+'])
            else:
                subprocess.call(['amixer', '-q', 'set', 'Attenuation', '1dB-'])
        clkLastState = clkState
        GPIO.wait_for_edge(clk, GPIO.BOTH, timeout=5000)
finally:
    GPIO.cleanup()