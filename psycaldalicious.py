# Image Projection onto Sphere
# https://en.wikipedia.org/wiki/Equirectangular_projection
# Download the test image from the Wikipedia page!
# FB36 - 20160731
import math, random
import numpy as np
import serial
import serial.tools.list_ports
import serial
import time
import keyboard
ser = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=500000
)
if ser.isOpen():
    ser.close()
ser.open()
ser.isOpen()
ser.write('2\n')
ser.write('0 90\n')
time.sleep(0.1)
ser.write('0 15\n')
time.sleep(0.1)
ser.write('0 345\n')
time.sleep(0.1)
ser.write('0 15\n')
time.sleep(0.1)

lng = 15
lat = 0
dir0 = False
dir1 = False
speed0 = 1
speed1 = 5

pattern = 0
patterns = [0,1]

i = 0
while(True):
    print('%d %d'%(lng, lat))
    ser.write("0 " + str(lng) + "\n")
    time.sleep(0.02)
    ser.write("1 " + str(lat) + "\n")
    time.sleep(0.02)
    i = i+1
    if pattern==0:
        if dir0:
            lng -= speed0
        else:
            lng += speed0
        if dir1:
            lat -= 0.1*speed1
        else:
            lat += 0.1*speed1
        if lng<15:
            dir0 = not dir0
            lng = 26
            speed0 =  random.uniform(1,10)
        if lng>345:
            dir0 = not dir0
            lng = 334
            speed0 =  random.uniform(1,10)
        if lat>130:
            dir1 = not dir1
            lat = 120
            speed1 =  random.uniform(1,10)
        if lat<0:
            dir1 = not dir1
            lat = 0
            speed1 =  random.uniform(1,10)
    elif pattern==1:
        if dir0:
            lng -= np.sin(i/float(speed0))
        else:
            lng += np.sin(i/float(speed0))
        if dir1:
            lat -= np.cos(i/float(speed1))
        else:
            lat += np.cos(i/float(speed1))
        if lng<15:
            dir0 = not dir0
            lng = 26
            speed0 =  random.uniform(1,100)
        if lng>345:
            dir0 = not dir0
            lng = 334
            speed0 =  random.uniform(1,100)
        if lat>130:
            dir1 = not dir1
            lat = 120
            speed1 =  random.uniform(1,1000)
        if lat<0:
            dir1 = not dir1
            lat = 0
            speed1 =  random.uniform(1,1000)

    try:
        if keyboard.is_pressed('q'):
            break
        else:
            pass
    except:
        break
    try:
        if keyboard.is_pressed('p'):
            pattern = pattern+1
            if pattern>len(patterns):
                pattern = 0
        else:
            pass
    except:
        pass
ser.write('3 \n')
ser.close()
