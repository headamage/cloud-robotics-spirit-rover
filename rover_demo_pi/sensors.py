from time import sleep
import spirit_core
import spirit_pixels as pixels
import sys
from random import randrange
s=spirit_core.Spirit()

def exceptionHandler(exception_type, exception, traceback, debug_hook=sys.excepthook):
	print "%s: %s" % (exception_type.__name__, exception)
s.i2c_process_delay(15)

def readSensors(): #this will read all sensors on the rover. There seems to be a gyro and accelerometer also but I don't know how to get those.
	sensorReadings = [ s.surf_left_0(), s.surf_left_1(), s.surf_right_0(), s.surf_right_1(), s.surf_rear_0(), s.surf_rear_1(), s.rangefinder(), s.amb_left(), s.amb_right(), s.amb_rear(), round(s.power_voltage(), 2) ]
	return sensorReadings

def readSurface(): #this will return only the surface sensors along with range. use this if you prefer a lighter version for navigation only.
	surfaceReadings = [s.surf_left_0(), s.surf_left_1(), s.surf_right_0(), s.surf_right_1(), s.surf_rear_0(), s.surf_rear_1(), s.rangefinder()]
	return surfaceReadings

if __name__ == "__main__" :
	while True:
		print readSensors()
