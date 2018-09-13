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
        self.calFile = open('calibration.json', 'r')
        self.calibrationData = json.load(self.calFile)

    def stopServos(self):
        self.pwm.set_pwm(self.LSERVO, 0, 0)
        self.pwm.set_pwm(self.RSERVO, 0, 0)

    def setSpeeds(self, left, right):
        # print("left: " + str(left))
        # print("right: " + str(right))
        self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

    #all of this is for calibration    

# def setSpeedsRPS(rpsLeft, rpsRight):
        #self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        #self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

# def setSpeedsIPS(ipsLeft, ipsRight):
        #self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        #self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

# def setSpeedsvw(v, w):
        #self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        #self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

    def printCalibrationData(self):
        print(self.calibrationData['left']['0.37524266106022125'])
        
    def retrieveJSONSpeed(self, side, rps):
        
