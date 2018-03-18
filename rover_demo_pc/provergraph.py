import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import random, socket
graph_addr  = ('192.168.11.21', 10001)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(graph_addr)
## Populate the plot arrays with 0 
i=0
data0 = [] #rangefinder
data1 = [] #left surface 0
data2 = [] #left surface 1
data3 = [] #right surface 0
data4 = [] #right surface 1
data5 = [] #rear surface 0
data6 = [] #rear surface 1
data7 = [] #left motor
data8 = [] #right motor
data9 = [] #left ambient
data10= [] #right ambient
data11= [] #rear ambient
data12= [] #battery volts

for i in range (0,100) :
	data0.append(0)
	data1.append(0)
	data2.append(0)
	data3.append(0)
	data4.append(0)
	data5.append(0)
	data6.append(0)
	data7.append(0)
	data8.append(0)
	data9.append(0)
	data10.append(0)
	data11.append(0)
	data12.append(0)

#Widget design
win = pg.GraphicsWindow() #Top row of graphs
win.setWindowTitle('Rover Sensors and Motors')
p0 = win.addPlot(colspan=3, title="Range Finder (mm)")
curve0 = p0.plot(data0, pen='c')  

win.nextRow() #Second row of graphs
p1 = win.addPlot(title="Left Surface Sensors")
curve1 = p1.plot(data1, pen='m')
curve2 = p1.plot(data2, pen='y')
p2 = win.addPlot(title="Right Surface Sensors")
curve3 = p2.plot(data3, pen='m')
curve4 = p2.plot(data4, pen='y')
p3 = win.addPlot(title="Rear Surface Sensors")
curve5 = p3.plot(data5, pen='m')
curve6 = p3.plot(data6, pen='y')

win.nextRow() #Third row of graphs
p4 = win.addPlot(colspan=3, title="Motors")
curve7 = p4.plot(data7, pen='r')
curve8 =  p4.plot(data8, pen='g')

win.nextRow() #Fourth row of graphs
p5 = win.addPlot(title="Left Ambient Sensor")
p6 = win.addPlot(title="Right Ambient Sensor")
p7 = win.addPlot(title="Rear Ambient Sensor")
curve9 = p5.plot(data9, pen='r')
curve10 = p6.plot(data10, pen='g')
curve11 = p7.plot(data11, pen='b')

win.nextRow() #Fifth row of graphs
p8 = win.addPlot(colspan=3, title="Battery Voltage (volts)")
curve12 = p8.plot(data12)



ptr1 = 0
ptr2 = 0
def update1(left0,left1,right0,right1,rear0,rear1,rangefinder,leftambient,rightambient,rearambient,volts):
	global data0, data1, data2, data3, data4, data5, data6, data9, data10, data11, data12, curve0, curve1, curve2, curve3, curve4, curve5, curve6, curve9, curve10, curve11, curve12, ptr1
	
	data0[:-1] = data0[1:]
	if (int(rangefinder) == 0):
		rangefinder = 999
	data0[-1] = int(rangefinder)

	data1[:-1] = data1[1:]  
	data1[-1] = int(left0)
	
	data2[:-1] = data2[1:]
	data2[-1] = int(left1) 

	data3[:-1] = data3[1:]
	data3[-1] = int(right0)

	data4[:-1] = data4[1:]
	data4[-1] = int(right1)    

	data5[:-1] = data5[1:]
	data5[-1] = int(rear0)    

	data6[:-1] = data6[1:]
	data6[-1] = int(rear1)
	
	data9[:-1] = data9[1:]
	data9[-1] = int(leftambient)

	data10[:-1] = data10[1:]
	data10[-1] = int(rightambient)

	data11[:-1] = data11[1:]
	data11[-1] = int(rearambient)
   
	data12[:-1] = data12[1:]
	data12[-1] = float(volts)


	curve0.setData(data0)
	curve0.setPos(ptr1, 0)    
	curve1.setData(data1)
	curve1.setPos(ptr1, 0)
	curve2.setData(data2)
	curve2.setPos(ptr1, 0)
	curve3.setData(data3)
	curve3.setPos(ptr1, 0)
	curve4.setData(data4)
	curve4.setPos(ptr1, 0)
	curve5.setData(data5)
	curve5.setPos(ptr1,0)
	curve6.setData(data6)
	curve6.setPos(ptr1, 0)

	curve9.setData(data9)
	curve9.setPos(ptr1, 0)
	curve10.setData(data10)
	curve10.setPos(ptr1, 0)
	curve11.setData(data11)
	curve11.setPos(ptr1, 0)
	curve12.setData(data12)
	curve12.setPos(ptr1, 0)	
	
	ptr1 += 1

def update2(leftMotor,rightMotor):
	global curve7, curve8, ptr2

	data7[:-1] = data7[1:]
	data8[:-1] = data8[1:]
	data7[-1] = int(leftMotor)
	data8[-1] = int(rightMotor)

	curve7.setData(data7)
	curve7.setPos(ptr2, 0)
	curve8.setData(data8)
	curve8.setPos(ptr2, 0)
	ptr2 += 1

leftMotorVal = 0
rightMotorVal= 0

# update all plots
def update():
	global leftMotorVal, rightMotorVal
	sensors, address = sock.recvfrom(4096)
	sensorValues = sensors.split(',')
	#print sensorValues
	if (sensorValues[0] == "Motor"):
		update2(sensorValues[1],sensorValues[2])
		leftMotorVal = int(sensorValues[1])
		rightMotorVal = int(sensorValues[2])
	else:
		update1(sensorValues[0], sensorValues[1],sensorValues[2], sensorValues[3],sensorValues[4], sensorValues[5],sensorValues[6],sensorValues[7],sensorValues[8],sensorValues[9],sensorValues[10])
		update2(leftMotorVal,rightMotorVal)


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)
## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

