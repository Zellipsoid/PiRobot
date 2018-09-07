import time
import Adafruit_PCA9685
import signal
import math

class Servos(object):

    # def __init__(self):

    def setSpeeds(left, right):
        pwm.set_pwm(LSERVO, 0, math.floor(left / 20 * 4096))
        pwm.set_pwm(RSERVO, 0, math.floor((3 - right) / 20 * 4096))

# def calibrateSpeeds():

# def setSpeedsRPS(rpsLeft, rpsRight):

# def setSpeedsvw(v, w):
