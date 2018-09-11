import time
import Adafruit_PCA9685
import signal
import math
import encoders
import json

class Servos(object):

    def __init__(self):
        # Initialize the servo hat library.
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.LSERVO = 0
        self.RSERVO = 1
        self.calibrating = false
        self.wheelTicksLeft = 0
        self.wheelTicksRight = 0
    def stopServos(self):
        self.pwm.set_pwm(self.LSERVO, 0, 0)
        self.pwm.set_pwm(self.RSERVO, 0, 0)
    def setSpeeds(self, left, right):
        # print("left: " + str(left))
        # print("right: " + str(right))
        self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

    #all of this is for calibration
    def leftTick(self):
        if (self.calibrating):
            self.wheelTicksLeft += 1
    def rightTick(self):
        if (self.calibrating):
            self.wheelTicksRight += 1
    def calibrateSpeeds(self):
        encForCal = encoders.Encoders()

# def setSpeedsRPS(rpsLeft, rpsRight):

# def setSpeedsvw(v, w):
