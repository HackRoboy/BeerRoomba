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
pinDirection = 22
pinPWM = 24
pinDisable = 26

def driveMotorForwards():
    GPIO.output(pinDirection, True)
    GPIO.output(pinPWM, True)
    GPIO.output(pinDisable, False)


def driveMotorBackwards():
    GPIO.output(pinDirection, False)
    GPIO.output(pinPWM, True)
    GPIO.output(pinDisable, False)


def stopMotor():
    GPIO.output(pinDirection, False)
    GPIO.output(pinPWM, False)
    GPIO.output(pinDisable, True)


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
                driveMotorForwards()
            elif key == 'j':
                driveMotorBackwards()
            elif key == 'n':
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

