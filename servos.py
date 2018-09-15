import time
import Adafruit_PCA9685
import signal
import math
import encoders
import json
import bisect
from collections import OrderedDict

class Servos(object):

    def __init__(self):
        # Initialize the servo hat library.
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.LSERVO = 0
        self.RSERVO = 1
        self.calibrationDataLeft = []
        self.calibrationDataRight = []
        self.loadJSON()
        #  = json.load(open('calibration.json', 'r'), object_pairs_hook=OrderedDict) #opens json as ordered dict
        # self.calibrationData['right'] = {float(k):v for k, v in self.calibrationData['right'].items()} #converts keys from strings to floats for right side
        # self.calibrationData['left'] = {float(k):v for k, v in self.calibrationData['left'].items()} #converts keys from strings to floats for left side

    def loadJSON(self):
        left = False
        right = False
        with open('calibration.json', 'r') as json:
            for line in json:
                if "left" in line:
                    left = True
                    right = False
                    continue
                elif "right" in line:
                    right = True
                    left = False
                    continue
                elif "{" in line or "}" in line:
                    continue
                else:
                    numberString = line.replace(",", "").replace("\"", "").replace(" ", "").replace("\n", "")
                    numberArray = numberString.split(":")
                    numberArray[0] = float(numberArray[0])
                    numberArray[1] = float(numberArray[1])
                    if (left):
                        self.calibrationDataLeft.append(tuple(numberArray))
                    if (right):
                        self.calibrationDataRight.append(tuple(numberArray))
                                                                                                                                        

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
        print(self.calibrationDataLeft)
        print(self.calibrationDataRight)
        
    def retrieveJSONSpeed(self, side, rps): #side is string
        index = bisect.bisect_left(list(self.calibrationData[side].keys()), rps) #finds first index that has key larger than rps
        value = next( i for i, v in enumerate(self.calibrationData[side]) if i == index ) # loads key for that index
        valueMinusOne = next( i for i, v in enumerate(self.calibrationData[side]) if i == index - 1 ) #and the key for one lower
        print(index)
        if abs(rps - valueMinusOne) - abs(rps - value) >= 0: #checks which is closest to rps passed in
            return next( v for i, v in enumerate(self.calibrationData[side]) if i == index) #returns value of next larger key
        else:
            return next( v for i, v in enumerate(self.calibrationData[side]) if i == index -1) #returns value for the key one lower


        # return min(abs(rps - list(self.calibrationData[side].values())[index]), abs(rps - list(self.calibrationData[side].values())[index - 1]))
        
