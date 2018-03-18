import socket, sys, time, random
from multiprocessing import Process, Pipe
from time import sleep

# Network variables
ai_addr = ('192.168.11.21', 10000)
rover_addr  = ('192.168.11.13', 10000)
graph_addr = ('192.168.11.21', 10001)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ai_addr)

# Basic run parameters
runBeforeAct = 2000
sensorThres = 400
surfBase = 0
#Define motor speeds
def motorMove(l, r):
	motorParams = ["Motor"]
	motorParams.append(str(l))
	motorParams.append(str(r))
	motorParams = ','.join(str(e) for e in motorParams)
	motorSend = sock.sendto(motorParams, rover_addr)
	graphSend = sock.sendto(motorParams, graph_addr)

def pixelCtrl(led_id, hue, power):
	pixelParams = ["Pixel"]
	pixelParams.append(str(led_id))
	pixelParams.append(str(hue))
	pixelParams.append(str(power))
	pixelParams = ','.join(str(e) for e in pixelParams)
	pixelSend = sock.sendto(pixelParams, rover_addr)

def servoPan(angle):
	servoParams = ["ServoPan"]
	servoParams.append(angle)
	servoParams = ','.join(str(e) for e in servoParams)
	servoSend = sock.sendto(servoParams, rover_addr)

def servoGrip(angle):
	servoParams = ["ServoGrip"]
	servoParams.append(angle)
	servoParams = ','.join(str(e) for e in servoParams)
	servoSend = sock.sendto(servoParams, rover_addr)

def servoTilt(angle):
	servoParams = ["ServoTilt"]
	servoParams.append(angle)
	servoParams = ','.join(str(e) for e in servoParams)
	servoSend = sock.sendto(servoParams, rover_addr)

def leftFlash(status):
	if (status == "on"):
		br=5
	if (status == "off"):
		br=0
	pixelCtrl(5, 50, br)
	sleep(0.1)
	pixelCtrl(6, 50, br)
	sleep(0.1)
	pixelCtrl(7, 50, br)
	sleep(0.1)

def rightFlash(status):
	if (status == "on"):
		br=5
	if (status == "off"):
		br=0
	pixelCtrl(17,50,br)
	sleep(0.1)
	pixelCtrl(18,50,br)
	sleep(0.1)
	pixelCtrl(19,50,br)
	sleep(0.1)

def escapeLeft(): # Escape move from left edge detection
	global surfBase
	motorMove(-120, -120)
	sleep(0.3)
	motorMove(-50, -120)
	print "Starting emergency reverse"
	for m in range (0, 20):
		data, address = sock.recvfrom(4096)
		sensorValues = data.split(',')
		if ( (int(sensorValues[4]) <= (surfBase - sensorThres)) or (int(sensorValues[4]) >= (surfBase + sensorThres)) or (int(sensorValues[5]) <= (surfBase - sensorThres)) or (int(sensorValues[5]) >= (surfBase + sensorThres)) ):
			print "[Left] STOP!!! Cliff behind me."
			motorMove(90, 90)
			pixelCtrl(13, 50, 5)
			sleep(0.2)
			data, address = sock.recvfrom(4096)
			sensorValues = data.split(',')
			surfBase = ((int(sensorValues[0]) + int(sensorValues[1]) + int(sensorValues[2]) + int(sensorValues[3]) + int(sensorValues[4]) + int(sensorValues[5]) ) / 6)
	motorMove(0, 0)
	sleep(0.1)
	pixelCtrl(13, 50, 0)
	sleep(0.1)

def escapeRight(): # Escape move from right edge detection
	global surfBase
	motorMove(-120, -120)
	sleep(0.3)
	motorMove(-120, -50)
        print "Starting emergency reverse"
	for m in range (0, 20):
		data, address = sock.recvfrom(4096)
		sensorValues = data.split(',')
		if ( (int(sensorValues[4]) <= (surfBase - sensorThres)) or (int(sensorValues[4]) >= (surfBase + sensorThres)) or (int(sensorValues[5]) <= (surfBase - sensorThres)) or (int(sensorValues[5]) >= (surfBase + sensorThres)) ):
			print "[Right] STOP!!! Cliff behind me."
			motorMove(90, 90)
			pixelCtrl(25, 50, 5)
			sleep(0.2)
			data, address = sock.recvfrom(4096)
			sensorValues = data.split(',')
			surfBase = ((int(sensorValues[0]) + int(sensorValues[1]) + int(sensorValues[2]) + int(sensorValues[3]) + int(sensorValues[4]) + int(sensorValues[5]) ) / 6)
	motorMove(0, 0)
	sleep(0.1)
	pixelCtrl(25, 50, 0)
	sleep(0.1)

def escapeRange():
	print "Hit the brakes!! Obstacle in the path!"
	choice = random.randint(0,1)
	if ( choice == 0):
		#print "chose left escape"
		escapeLeft()
		#sleep(5)
	if (choice == 1):
		#print "chose right escape"
		escapeRight()
		#sleep(5)
def moveLoop():
	global surfBase
	data, address = sock.recvfrom(4096)
	sensorValues = data.split(',')
	#print sensorValues
	surfBase = ((int(sensorValues[0]) + int(sensorValues[1]) + int(sensorValues[2]) + int(sensorValues[3]) + int(sensorValues[4]) + int(sensorValues[5]) ) / 6)
	print "Surface base value is: ", surfBase, "\t Threshold: ", sensorThres
	while True:
		servoPan(0)
		servoTilt(20)
		motorMove(80, 80) # start the motors after timestamp
		timestamp = int(round(time.time() * 1000))
		while ( int(round(time.time()*1000)) < (timestamp + runBeforeAct) ):
			data, address = sock.recvfrom(4096)
			sensorValues = data.split(',')
			#print sensorValues
			#print "Range: ", sensorValues[6]
			if ( int(sensorValues[0]) <= (surfBase - sensorThres) or int(sensorValues[0]) >= (surfBase + sensorThres) or int(sensorValues[1]) <= (surfBase - sensorThres) or int(sensorValues[1]) >= (surfBase + sensorThres) ):
				print "Hit the brakes!!! There is a cliff on the left! Starting emergency reverse."
				#print "Left sensor value: ", sensorValues[0], sensorValues[1]
				motorMove(0, 0)
				sleep(0.1)
				leftFlash("on")
				escapeLeft()
				leftFlash("off")
				print "Phew! I am safe from cliff on the left. Resume roaming."
				timestamp = round(time.time() * 1000)
			if ( int(sensorValues[2]) <= (surfBase - sensorThres) or int(sensorValues[2]) >= (surfBase + sensorThres) or int(sensorValues[3]) <= (surfBase - sensorThres) or int(sensorValues[3]) >= (surfBase + sensorThres) ):
				print " Hit the brakes!!! There is a cliff on the right! Starting emergency reverse"
				#print "Right sensor value: ", sensorValues[2], sensorValues[3]
				motorMove(0, 0)
				sleep(0.1)
				rightFlash("on")
				escapeRight()
				rightFlash("off")
				print "Phew! I am safe from cliff on the right. Resume roaming."
				timestamp = round(time.time() * 1000)
			if ( int(sensorValues[6]) != 0 and int(sensorValues[6]) <= 200 ):
				#print "Range sensor is: (mm) ", sensorValues[6]
				motorMove(0, 0)
				sleep(0.2)
				choice = random.randint(0,10)
				if ( choice <= 6):
					#print "I will do action 1"
					servoPan(30)
					sleep(0.25)
					servoPan(-50)
					sleep(0.25)
					servoPan(0)
					sleep(0.25)
				if ( choice >= 7):
					#print "I will do action 2"
					servoTilt(80)
					sleep(0.25)
					servoTilt(-40)
					sleep(0.25)
					servoTilt(30)
					sleep(0.25)
				escapeRange()
				timestamp = round(time.time() * 1000)

if __name__ == "__main__" :
	try:
		moveLoop()

	except KeyboardInterrupt:
		print "Roaming terminated by user."
		motorMove(0, 0)
