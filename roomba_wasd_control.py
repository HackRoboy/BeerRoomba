import readchar

import rospy
from std_msgs.msg import Int8

## Motor Stuff
import time
# import pigpio
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT, initial=False)
GPIO.setup(24, GPIO.OUT, initial=False)
GPIO.setup(26, GPIO.OUT, initial=False)

# definition of H-Bridge IC pins
pinDirection = 25 # physical 22
pinPWM = 8      # physical 24   
pinDisable = 7  # physical 26 

# initialization of GPIO pins
pi.set_mode(pinDirection, pigpio.OUTPUT)
pi.set_mode(pinPWM, pigpio.OUTPUT)
pi.set_mode(pinDisable, pigpio.OUTPUT)


def driveMotorForwards():
    pi.write(pinDirection, False)
    pi.write(pinPWM, False)
    pi.write(pinDisable, True)


def driveMotorBackwards():
    pi.write(pinDirection, True)
    pi.write(pinPWM, False)
    pi.write(pinDisable, True)


def stopMotor():
    pi.write(pinDirection, True)
    pi.write(pinPWM, False)
    pi.write(pinDisable, False)

def talker():
    pub = rospy.Publisher('pet_roomba3000', Int8, queue_size=10)
    rospy.init_node('RoombaWASD', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        key = readchar.readkey()
        key = key.lower()

        if key in ('wasdujn'):
            if key == 'w':  # Forward
                print "w"
                pub.publish(1)
            elif key == 'a':  # Left
                print "a"
                pub.publish(4)
            elif key == 'd':  # Right
                print "d"
                pub.publish(5)
            elif key == 's':  # stand still
                print "s"
                pub.publish(6)
            elif key == 'u':
                print "u"
                driveMotorForwards()
            elif key == 'j':
                print "j"
                driveMotorBackwards()
            elif key == 'n':
                print "n"
                stopMotor()

        elif key == 'p':
            print "stop"
            break
        rate.sleep()
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

