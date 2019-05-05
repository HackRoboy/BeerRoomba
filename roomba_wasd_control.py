import readchar

import rospy
from std_msgs.msg import Int8

## Motor Stuff
import time
import pigpio

pi = pigpio.pi()

# definition of H-Bridge IC pins
pinDirection = 22
pinPWM = 24
pinDisable = 26

# initialization of GPIO pins
pi.set_mode(pinsA[0], pigpio.OUTPUT)
pi.set_mode(pinsA[1], pigpio.OUTPUT)
pi.set_mode(pinsA[2], pigpio.OUTPUT)


def driveMotorForwards():
    pi.write(pinDirection, True)
    pi.write(pinPWM, True)
    pi.write(pinDisable, False)


def driveMotorBackwards():
    pi.write(pinDirection, False)
    pi.write(pinPWM, True)
    pi.write(pinDisable, False)


def stopMotor():
    pi.write(pinDirection, False)
    pi.write(pinPWM, False)
    pi.write(pinDisable, True)


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

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

