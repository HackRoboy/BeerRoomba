import serial
import serial.tools.list_ports
import time

ports = list(serial.tools.list_ports.comports())
print(ports[0])
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=500000)
ser.write('0 0\n')
ser.write('1 120\n')
ser.write('3\n')
i = 15
j = 120
dir0 = False
dir1 = True
while True:
    ser.write('0 '+str(i)+'\n')
    if not dir0:
        i = i+1
    else:
        i = i-1

    if i<15:
        i= 15
        dir0 = not dir0
    if i>345:
        i = 345
        dir0 = not dir0
    time.sleep(0.02)
    ser.write('1 '+str(j)+'\n')
    if not dir1:
        j = j+1
    else:
        j = j-1

    if j<100:
        j= 100
        dir1 = not dir1
    if j>160:
        j = 160
        dir1 = not dir1
ser.close()
