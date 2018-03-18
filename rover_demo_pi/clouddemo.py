#you can put this script in rc.local to automatically launch it when the pi boots but it is not recommended since it will impact battery life.
#It may also interfere with anything else you are trying to do with the rover. Only run it when you want to experiment with cloud robotics.

import socket, sys, time, spirit_core
import sensors as sensors
from time import sleep
from multiprocessing import Process, Pipe
import spirit_pixels as pixels
s= spirit_core.Spirit()
def exceptionHandler(exception_type, exception, traceback, debug_hook=sys.excepthook):
  print "%s: %s" % (exception_type.__name__, exception)
s.i2c_process_delay(15)

# Network variables
rover_addr = ("192.168.11.13", 10000) #set this to match the IP of your rover
server_addr = ("192.168.11.21", 10000) #set this to match the IP of the PC that will run your AI or manual control scripts
graph_addr = ("192.168.11.21", 10001) #set this to match the IP of the PC that will run your sensor graphs. Typically same as the control PC.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket
sock.bind(rover_addr)

def netSens(): #this will constantly read all sensors and send them over wifi to the PC that runs graphs and control.
	try: #lets turn on some pixels to indicate our script is live. Some pixels will light blue on left and right wings.
		pixels.hue_pixel(12,240,5)
		sleep(0.1)
		pixels.hue_pixel(24,240,5)
		sleep(0.1)
		pixels.hue_pixel(11,240,5)
                sleep(0.1)
                pixels.hue_pixel(23,240,5)
		sleep(0.1)
		while True:
			sensorReadings = ','.join(str(e) for e in sensors.readSensors())
			serverSend = sock.sendto(sensorReadings, server_addr)
			graphSend = sock.sendto(sensorReadings, graph_addr)
			#conn.send(int(time.clock()))
			sleep(0.075)
			#print sensorReadings
	except KeyboardInterrupt:
		print "exiting net sense"

def netCtrl(): #this will constantly listen on the pi address for motor and servo instructions.
	try:
		s.servo_speed(4000)
		pong = 0
		while True:
			data, address = sock.recvfrom(4096)
			data = data.split(',')
			if (data[0] == "Motor"):
				s.motors( int(data[1]), int(data[2]) )
				#print "Setting motors to: ", data[1], " - ", data[2] 
			#if (data[0] == "pong"): # periodic RTT report based on the RPi CPU clock
				#pong = pong + 1
	     			#if (pong == 20):
				#	pong = 0 # reset counter
					#timestamp = child_conn.recv()
					#print timestamp
					#timestamprtt = time.clock()
					#rtt = timestamprtt - timestamp
					#print "Network roundtrip is: ", rtt
			if (data[0] == "Pixel"):
                                pixels.hue_pixel(data[1],data[2],data[3])
				sleep(0.1)
                                #print "Setting pixel: ", data[1], "to hue: ", data[2], "and brightness: ", data[3]
			if (data[0] == "ServoPan"):
				s.servo_pan(data[1])
				sleep(0.25)
			if (data[0] == "ServoTilt"):
				s.servo_tilt(data[1])
				sleep(0.25)
			if (data[0] == "ServoGrip"):
				s.servo_grip(data[1])
				sleep(0.25)

	except KeyboardInterrupt:
		print "exiting net motor"


if __name__ == '__main__':
	try: #lets give a thread for each function so they run independently and improve the performance of the pi a bit.
		#parent_conn, child_conn = Pipe()
		p1 = Process(target=netSens)
		p1.start()
		p2 = Process(target=netCtrl)
		p2.start()
		p1.join()
		p2.join()
	except KeyboardInterrupt: #let's turn off the blue pixels on the wing to indicate that we are not active anymore.
		print "Terminating main thread"
		s.motors(0,0)
		sleep(0.1)
		pixels.hue_pixel(12,240,0)
		sleep(0.1)
		pixels.hue_pixel(24,240,0)
		sleep(0.1)
                pixels.hue_pixel(11,240,0)
                sleep(0.1)
                pixels.hue_pixel(23,240,0)
