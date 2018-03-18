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
	#leftSurf0 = s.surf_left_0()
	#sleep(0.05)
	#leftSurf1 =  s.surf_left_1()
	#sleep(0.05)
	#rightSurf0 = s.surf_right_0()
	#sleep(0.05)
	#rightSurf1 =  s.surf_right_1()
	#sleep(0.05)
	#rearSurf0 = s.surf_rear_0()
	#sleep(0.05)
	#rearSurf1 =  s.surf_rear_1()
	#sleep(0.05)
	#range = s.rangefinder()
	#sleep(0.05)
	#leftLight = s.amb_left()
	#sleep(0.05)
	#rightLight = s.amb_right()
	#sleep(0.05)
	#rearLight = s.amb_rear()
	#sleep(0.05)
	#volts = round(s.power_voltage(), 2)
	sensorReadings = [ s.surf_left_0(), s.surf_left_1(), s.surf_right_0(), s.surf_right_1(), s.surf_rear_0(), s.surf_rear_1(), s.rangefinder(), s.amb_left(), s.amb_right(), s.amb_rear(), round(s.power_voltage(), 2) ]
	return sensorReadings

def readSurface(): #this will return only the surface sensors along with range. use this if you prefer a lighter version for navigation only.
	surfaceReadings = [s.surf_left_0(), s.surf_left_1(), s.surf_right_0(), s.surf_right_1(), s.surf_rear_0(), s.surf_rear_1(), s.rangefinder()]
	return surfaceReadings

if __name__ == "__main__" :
	while True:
		print readSensors()
