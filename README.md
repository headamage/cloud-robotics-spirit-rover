# cloud-robotics-spirit-rover

This guide assumes you have completed the setup of the Spirit Rover according to Plumgeek's documentation.
Make sure the Raspberry Pi boots up and you can SSH to it over WiFi. I assume you know how to work with wpa_supplicant to connect the pi to WiFi at boot.

This code will allow you to stream sensor data from the rover to a PC where all the processing is performed and motor/servo instructions are sent back to the rover. The code also allows for manual control of the rover if the user wishes to do that. The autonomous mode behaves similarly to demo mode 2 of the shipping code except instead of running the logic on the arduino, it runs on a PC.

Feel free to clone and modify the code.

File locations are as follows:

manualrover.py should be on the PC controlling the rover
proverai.py should be on the PC controlling the rover
provergraph.py should be on the PC controlling the rover

clouddemo.py should be on the raspberry pi in ~/rover/democode since it uses methods from other python scripts in that folder
navlights.py should be on the raspberry pi in ~/rover/democode since it uses methods from other python scripts in that folder

Setup:

Add the following line to /etc/rc.local before the "exit 0" at the end of the file:

python /home/pi/rover/democode/navlights.py

This will startup the navigation lights as soon as the pi boots up so you get a visual confirmation that the pi is ready and you can ssh to it. 

Flash the arduino with the provided PiControl sketch and power cycle the rover.

When the rover boots up and you see the navigation lights, SSH to the Pi and execute clouddemo.py
This will start the sensor data streaming to the PC over WiFi.

At this point you can run the provergraph.py on the PC to see the sensor data.
Executing proverai.py will automatically run the rover performing surface sensing to avoid edges and range finding to detect and avoid obstacles.
Alternatively, you can execute manualrover.py and take manual control of the rover using WASD for motor control and UJHKG for servos

