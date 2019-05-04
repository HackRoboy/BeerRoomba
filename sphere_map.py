# Image Projection onto Sphere
# https://en.wikipedia.org/wiki/Equirectangular_projection
# Download the test image from the Wikipedia page!
# FB36 - 20160731
import math, random
from PIL import Image
import numpy as np
import serial
import serial.tools.list_ports
import sys
import glob
import serial


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

# ports = serial_ports()
# print(ports)
#
# ser = serial.Serial(
#     port=ports[0],
#     baudrate=115200,
#     parity=serial.PARITY_ODD,
#     stopbits=serial.STOPBITS_ONE,
#     bytesize=serial.EIGHTBITS
# )
# if ser.isOpen():
#     ser.close()
# ser.open()
# ser.isOpen()
#
# imgxOutput = 768; imgyOutput = 768
# pi2 = math.pi * 2
# # 3D Sphere Rotation Angles (arbitrary)
# # xy = -pi2 * random.random()
# # xz = -pi2 * random.random()
# # yz = -pi2 * random.random()
# xy = 0
# xz = 0
# yz = 100.0 * np.pi/180.0
# sxy = math.sin(xy); cxy = math.cos(xy)
# sxz = math.sin(xz); cxz = math.cos(xz)
# syz = math.sin(yz); cyz = math.cos(yz)
# imageInput = Image.open("/home/letrend/Pictures/test.png")
# (imgxInput, imgyInput) = imageInput.size
# pixelsInput = imageInput.load()
# imageOutput = Image.new("RGB", (imgxOutput, imgyOutput))
# pixelsOutput = imageOutput.load()
# # define a sphere behind the screen
# xc = (imgxOutput - 1.0) / 2
# yc = (imgyOutput - 1.0) / 2
# zc = min((imgxOutput - 1.0), (imgyOutput - 1.0)) / 2
# r = min((imgxOutput - 1.0), (imgyOutput - 1.0)) / 2
# # define eye point
# xo = (imgxOutput - 1.0) / 2
# yo = (imgyOutput - 1.0) / 2
# zo = -min((imgxOutput - 1.0), (imgyOutput - 1.0))
# xoc = xo - xc
# yoc = yo - yc
# zoc = zo - zc
# doc2 = xoc * xoc + yoc * yoc + zoc * zoc
# for yi in range(imgyOutput):
#     for xi in range(imgxOutput):
#         xio = xi - xo
#         yio = yi - yo
#         zio = 0.0 - zo
#         dio = math.sqrt(xio * xio + yio * yio + zio * zio)
#         xl = xio / dio
#         yl = yio / dio
#         zl = zio / dio
#         dot = xl * xoc + yl * yoc + zl * zoc
#         val = dot * dot - doc2 + r * r
#         if val >= 0: # if there is line-sphere intersection
#             if val == 0: # 1 intersection point
#                 d = -dot
#             else: # 2 intersection points => choose the closest
#                 d = min(-dot + math.sqrt(val), -dot - math.sqrt(val))
#                 xd = xo + xl * d
#                 yd = yo + yl * d
#                 zd = zo + zl * d
#                 x = (xd - xc) / r
#                 y = (yd - yc) / r
#                 z = (zd - zc) / r
#                 x0=x*cxy-y*sxy;y=x*sxy+y*cxy;x=x0 # xy-plane rotation
#                 x0=x*cxz-z*sxz;z=x*sxz+z*cxz;x=x0 # xz-plane rotation
#                 y0=y*cyz-z*syz;z=y*syz+z*cyz;y=y0 # yz-plane rotation
#                 lng = (math.atan2(y, x) + pi2) % pi2
#                 lat = math.acos(z)
#                 setpoint = '0 ' + str(int(lng)) + ' \n'
#                 ser.write(setpoint)
#                 setpoint = '1 ' + str(int(lat)) + ' \n'
#                 ser.write(setpoint)
#                 ix = int((imgxInput - 1) * lng / pi2 + 0.5)
#                 iy = int((imgyInput - 1) * lat / math.pi + 0.5)
#                 if pixelsInput[ix, iy][0]==0:
#                     print("lon %f lat %f"%(lng*180.0/np.pi,lat*180.0/np.pi))
#                 try:
#                     pixelsOutput[xi, yi] = pixelsInput[ix, iy]
#                 except:
#                     pass
#
# imageOutput.save("/home/letrend/Pictures/World.png", "PNG")


ports = serial_ports()
print(ports)

ser = serial.Serial(
    port=ports[0],
    baudrate=9600
)
if ser.isOpen():
    ser.close()
ser.open()
if ser.isOpen():
    setpoint = '0 180\n'
    my_str_as_bytes = str.encode(setpoint)
    print(setpoint)
    print(my_str_as_bytes)
    ser.write(setpoint)
else:
    print("serial not open")
ser.close()