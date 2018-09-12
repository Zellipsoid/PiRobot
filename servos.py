import time
import Adafruit_PCA9685
import signal
import math

class Servos(object):

    def __init__(self):
        # Initialize the servo hat library.
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.LSERVO = 0
        self.RSERVO = 1
    def stopServos(self):
        self.pwm.set_pwm(self.LSERVO, 0, 0)
        self.pwm.set_pwm(self.RSERVO, 0, 0)
    def setSpeeds(self, left, right):
        # print("left: " + str(left))
        # print("right: " + str(right))
        if left == 0 and right == 100:
            left = 1.5
            right = 1.6
        self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))
    #def setSpeedsIPS(self, ipsLeft, ipsRight):
        # print("ipsLeft: " + str(ipsLeft))
        # print("ipsRight: " + str(ipsRight))
        #if ipsLeft == 0 and ipsRight == 0:
             #ipsLeft = 1.5
             #ipsRight = 1.5
        #else:
            #calculate ips to ms
            #self.setSpeeds(..., ...) #based on calibrate speeds measurements 
        #self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        #self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

    # def setSpeedsRPS(rpsLeft, rpsRight):
        # print("rpsLeft: " + str(rpsLeft))
        # print("rpsRight: " + str(rpsRight))
        #if rpsLeft == 0 and rpsRight == 0:
             #rpsLeftt = 1.5
             #rpsRight = 1.5
        #else:
            #calculate rps to ms
            #self.setSpeeds(..., ...) #based on calibrate speeds measurements 
        #self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        #self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

   # def setSpeedsvw(v, w):
        # print("v: " + str(v))
        # print("w: " + str(w))
        #if v == 0 and w == 0:
             #v = 1.5
             #w = 1.5
        #else:
            #vL = v - wd #d being partial derivative of what?
            #vR = v + wd
            #self.setSpeeds(vL, vR) #based on calibrate speeds measurements 
        #self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        #self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))
