from pynput import keyboard
import proverai as rover
import sys
forward = False
back = False
left = False
right = False
gripper = False
tiltUp = False
tiltDown = False
panLeft = False
panRight = False

def on_press(key):
	global forward, back, left, right, panLeft, panRight, tiltUp, tiltDown, gripper
	try:
		#print('alphanumeric key {0} pressed'.format(key.char))
		if (format(key.char) == 'w'): #Forward stanza

			if (back == True):
				rover.motorMove(0, 0)
				#print "Forward and Back conflicting"

			if (back == False):
				forward = True
				rover.motorMove(100, 110)
				#print "Forward"

		if (format(key.char) == 'a'): #Left stanza
			if (forward == True):
				rover.motorMove(70, 110)
				#print "Forward left"

			if (back == True):
				#print "Back left"
				rover.motorMove(-70, -110)

			if (forward == False and back == False):
				left = True
				rover.motorMove(-40, 100)
				#print "Left"

		if (format(key.char) == 's'): #Back stanza

			if (forward == True):
				rover.motorMove(0, 0)
				#print "Back and Forward conflicting"

			if (forward == False):
				back = True
				rover.motorMove(-100, -100)
				#print "Back"

		if (format(key.char) == 'd'): #Right stanza
			if (forward == True):
				#print "Forward right"
				rover.motorMove(110, 70)
			if (back == True):
				#print "Back right"
				rover.motorMove(-110, -70)
			if (forward == False and back == False):
				right = True
				#print "Right"
				rover.motorMove(100, -40)
				
		if (format(key.char) == 'g'): #Gripper stanza
			if (gripper == False): #Check if gripper is engaged
				gripper = True # Set gripper status to engaged
				print "Turning gripper on"
				rover.servoGrip(90) #adjust this to suit the size of your object. Do not torture the servo!!
			else :
				gripper = False #Set gripper status to disengaged
				rover.servoGrip(0) #open the gripper
				print "Turning gripper off"
			
		if (format(key.char) == 'h'): #Pan left stanza
			if (panRight == True):
				panRight = False
				rover.servoPan(0)
				print "Looking right and turning to center"
			else:
				if (panLeft == True):
					print "I am already looking left!!"
				else:
					panLeft = True
					rover.servoPan(-50)
					print "Turning left"
			
		if (format(key.char) == 'k'): #Pan right stanza
			if (panLeft == True):
				panLeft = False
				rover.servoPan(0)
				print "Looking left and turning to center"
			else:
				if (panRight == True):
					print "I am already looking right!!"
				else:
					panRight = True
					rover.servoPan(50)
					print "Turning right"
			
		if (format(key.char) == 'u'): #Tilt up stanza
			if (tiltDown == True) :
				tiltDown = False
				rover.servoTilt(20)
			else:
				if (tiltUp == True):
					print "I am already looking up!"
				else:
					tiltUp = True
					rover.servoTilt(80)
			
		if (format(key.char) == 'j'): #Tilt down stanza
			if (tiltUp == True):
				tiltUp = False
				rover.servoTilt(20)
			else:
				if (tiltDown == True):
					print "I am already looking down!"
				else:
					tiltDown = True
					rover.servoTilt(-40)
			
	except AttributeError:
		print('Special key {0} pressed'.format(key))

def on_release(key):
	global forward, back, left, right
	try:
		if key == keyboard.Key.esc:
			sys.exit()
			return False
		key = str(key.char)
		if (key == 'w'):
			forward = False
			#print "Released forward"
			rover.motorMove(0, 0)
		if (key == 'a' and forward == True):
			left = False
			rover.motorMove(100,110)
			#print "Released left from forward"
		
		if (key == 'a' and back == True):
			right = False
			#print "Released right from back"
			rover.motorMove(-100, -110)
			
		if (key == 'a' and back == False and forward == False):
			right = False
			#print "Released right"
			rover.motorMove(0, 0)
		
		
		
		if (key == 's'):
			back = False
			#print "Released back"
			rover.motorMove(0, 0)
		if (key == 'd' and forward == True):
			right = False
			#print "Released right from forward"
			rover.motorMove(100, 110)
			
		if (key == 'd' and back == True):
			right = False
			#print "Released right from back"
			rover.motorMove(-100, -110)
			
		if (key == 'd' and back == False and forward == False):
			right = False
			#print "Released right"
			rover.motorMove(0, 0)
			
	except AttributeError:
		print "Special key {0} released".format(key)

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
	listener.join()
