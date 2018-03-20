#!/usr/bin/python
import random, signal, sys
from time import sleep
import spirit_core
import spirit_pixels as pixels   #pixel functions - read over spirit_pixels.py for more info
from random import randrange
s = spirit_core.Spirit()

def exceptionHandler(exception_type, exception, traceback, debug_hook=sys.excepthook):
  print "%s: %s" % (exception_type.__name__, exception)
s.i2c_process_delay(15)   #should leave this in place for all python scripts

# use this to set any pixel to any hue and brightness.
#In this case we are setting some pixels on the left wing to red and some pixels on the right wing to red.
#We also set the eyes to purple.
# pass pixel number (beginning with 0), pixel hue, and pixel brightness
sleep(2)
pixels.hue_pixel(3,0,5)
sleep(0.2)
pixels.hue_pixel(14,0,5)
sleep(0.2)
pixels.hue_pixel(4,0,5)
sleep(0.1)
pixels.hue_pixel(8,0,5)
sleep(0.2)
pixels.hue_pixel(9,0,5)
sleep(0.2)
pixels.hue_pixel(10,0,5)
sleep(0.2)
pixels.hue_pixel(15,120,5)
sleep(0.2)
pixels.hue_pixel(26,120,5)
sleep(0.2)
pixels.hue_pixel(16,120,5)
sleep(0.2)
pixels.hue_pixel(20,120,5)
sleep(0.2)
pixels.hue_pixel(22,120,5)
sleep(0.2)
pixels.hue_pixel(21,120,5)
sleep(0.2)
pixels.eyes(300,30) # eyes are different from other pixels. They only accept hue and brightness since the number of the pixels for the eyes is predefined.
#end of script
