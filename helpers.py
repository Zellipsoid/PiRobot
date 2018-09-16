import time
import Adafruit_PCA9685
import signal
import math
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
        self.calibrationDataLeftRPS = []
        self.calibrationDataRightRPS = []
        self.calibrationDataLeftMS = []
        self.calibrationDataRightMS = []
        self.loadJSON()
        self.wheelsDiameter = 2.61
        self.distanceBetweenWheels = 3.95

        self.velArrayRight = []
        self.velArrayLeft = []
        self.rightTicks = 0
        self.leftTicks = 0
        self.startTime = time.time()
        self.speedRecord = 2 #number of values to record in record of speed. Min val is 2. Bigger values are less instantaneous but more reliable.
        self.notMovingTimeout = 1 # time in s before declared as not moving if no encoders ticked. The smaller the value, the less accurate but the higher the response time.
        #for calibration
        self.calibrating = False
        self.wheelTicksLeft = 0
        self.wheelTicksRight = 0
        self.calibrationArrayRight = [] #these two arrays hold values for speed that will be averages for each speed increment and put into the json
        self.calibrationArrayLeft = []
        self.accuracy = 10 #will record speed this number of time and average result

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
                        self.calibrationDataLeftRPS.append(numberArray[0])
                        self.calibrationDataLeftMS.append(numberArray[1])
                    if (right):
                        self.calibrationDataRightRPS.append(numberArray[0])
                        self.calibrationDataRightMS.append(numberArray[1])                                                                                                                

    def stopServos(self):
        self.pwm.set_pwm(self.LSERVO, 0, 0)
        self.pwm.set_pwm(self.RSERVO, 0, 0)

    def setSpeeds(self, left, right):
        # print("left: " + str(left))
        # print("right: " + str(right))
        self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

    #all of this is for calibration    

    def setSpeedsRPS(self, rpsLeft, rpsRight):        
        self.setSpeeds(self.retrieveJSONSpeed("left", rpsLeft), self.retrieveJSONSpeed("right", rpsRight))
        

    def setSpeedsIPS(self, ipsLeft, ipsRight):
        self.setSpeedsRPS(ipsLeft / (self.wheelsDiameter * math.pi), ipsRight / (self.wheelsDiameter * math.pi))

    def setSpeedsVW(self, velocity, omega):
        if omega != 0:
            radius = velocity / omega
            vR = velocity + omega * (radius + self.distanceBetweenWheels / 2)
            vL = velocity + omega * (radius - self.distanceBetweenWheels / 2)
            self.setSpeedsIPS(vL, vR)
        else:
            self.setSpeedsIPS(velocity, velocity)

    def printCalibrationData(self):
        print(self.calibrationDataLeft)
        print(self.calibrationDataRight)
        
    def getMaxRPS(self):
        return min(self.calibrationDataRightRPS[len(self.calibrationDataRightRPS) - 1], self.calibrationDataLeftRPS[len(self.calibrationDataLeftRPS) - 1])
    
    def getMaxIPS(self):
        return min(self.calibrationDataRightRPS[len(self.calibrationDataRightRPS) - 1] * self.wheelsDiameter * math.pi, self.calibrationDataLeftRPS[len(self.calibrationDataLeftRPS) - 1] * self.wheelsDiameter * math.pi)

    def retrieveJSONSpeed(self, side, rps): #side is string
        if side == "left":
            index = bisect.bisect_left(self.calibrationDataLeftRPS, rps) #finds first index that has key larger than rps
            if index == len(self.calibrationDataLeftRPS):
                index -= 1
            if abs(rps - self.calibrationDataLeftRPS[index]) >= abs(rps - self.calibrationDataLeftRPS[index - 1]):
                return self.calibrationDataLeftMS[index - 1]
            else:
                return self.calibrationDataLeftMS[index]
        if side == "right":
            index = bisect.bisect_left(self.calibrationDataRightRPS, rps) #finds first index that has key larger than rps
            if index == len(self.calibrationDataRightRPS):
                index -= 1
            if abs(rps - self.calibrationDataRightRPS[index]) >= abs(rps - self.calibrationDataRightRPS[index - 1]):
                return self.calibrationDataRightMS[index - 1]
            else:
                return self.calibrationDataRightMS[index]

    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self, pin):
        #print("Left encoder ticked!")
        self.leftTicks += 1
        self.velArrayLeft.append((time.time(), self.leftTicks))
        if (len(self.velArrayLeft) > self.speedRecord):
            self.velArrayLeft = self.velArrayLeft[1:(self.speedRecord + 1)]
        if (self.calibrating):
            self.wheelTicksLeft += 1
            self.calibrationArrayLeft.append(self.getSpeeds()[0]) #append current left speed to array

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        #print("Right encoder ticked!")
        self.rightTicks += 1
        self.velArrayRight.append((time.time(), self.rightTicks))
        if (len(self.velArrayRight) > self.speedRecord):
            self.velArrayRight = self.velArrayRight[1:(self.speedRecord + 1)]
        if (self.calibrating):
            self.wheelTicksRight += 1
            self.calibrationArrayRight.append(self.getSpeeds()[1]) #append current right speed to array

    def resetCounts(self):
        self.rightTicks = 0
        self.leftTicks = 0

    def resetTime(self):
        self.startTime = time.time()

    def getCounts(self):
        return (self.leftTicks, self.rightTicks)

    def getDistanceTraveledRPS(self):
        return (self.leftTicks / 32, self.rightTicks / 32)
    
    def getDistanceTraveledIPS(self):
        return (self.leftTicks / 32 * self.wheelsDiameter * math.pi, self.rightTicks / 32 * self.wheelsDiameter * math.pi)

    def getSpeeds(self):
        totalTime = self.getElapsedTime()
        moving = self.isSpeedZero()
        leftLength = len(self.velArrayLeft)
        rightLength = len(self.velArrayRight)
        if rightLength > 0 and leftLength > 0 and totalTime > 0:
            if ((self.velArrayLeft[leftLength - 1][0] - self.velArrayLeft[0][0]) > 0 and (self.velArrayRight[rightLength - 1][0] - self.velArrayRight[0][0]) > 0):
                speedLeft = (self.velArrayLeft[leftLength - 1][1] - self.velArrayLeft[0][1]) / (self.velArrayLeft[leftLength - 1][0] - self.velArrayLeft[0][0])
                speedRight = (self.velArrayRight[rightLength - 1][1] - self.velArrayRight[0][1]) / (self.velArrayRight[rightLength - 1][0] - self.velArrayRight[0][0])
            else:
                return (0, 0)
            return (speedLeft / 32 * moving[0], speedRight / 32 * moving[1])
        else:
            return (0, 0)

    def getElapsedTime(self):
        return time.time() - self.startTime
    def isSpeedZero(self): #returns 0 for stopped, 1 for moving as a tuple (left, right)
        rightMoving = 1
        leftMoving = 1
        if (len(self.velArrayLeft) > 0):
            timeSinceLeft = time.time() - self.velArrayLeft[len(self.velArrayLeft) - 1][0]
        else:
            timeSinceLeft = 0
        if (len(self.velArrayRight) > 0):
            timeSinceRight = time.time() - self.velArrayRight[len(self.velArrayRight) - 1][0]
        else:
            timeSinceRight = 0
        if timeSinceRight > self.notMovingTimeout:
            rightMoving = 0
        if timeSinceLeft > self.notMovingTimeout:
            leftMoving = 0
        return (leftMoving, rightMoving)


    def calibrateSpeeds(self):
        self.wheelTicksLeft = 0
        self.wheelTicksRight = 0
        self.calibrating = True
        print('Starting calibration...')
        calibrationData = {} #dictionary containing calibration data
        calibrationData['left'] = {}
        calibrationData['right'] = {}
        rightStage = 1.2 #PWM freq for right
        leftStage = 1.8 #PWM freq for left
        print('CCW stage beginning...')
        while (rightStage < 1.5 and leftStage > 1.5):
            print('Collecting data for (' + str(leftStage) + ', ' + str(rightStage) + ')...')
            self.setSpeeds(leftStage, rightStage)
            print('Waiting for ticks...')
            while(self.wheelTicksLeft < self.accuracy + 1 and self.wheelTicksRight < self.accuracy + 1): #while loop is just to wait for more ticks
                pass
            print('Got the ticks!')
            averageSpeedLeft = sum(self.calibrationArrayLeft[-self.accuracy:]) / self.accuracy #averages last x elements of left array, left out first because it may not be accurate
            averageSpeedRight = sum(self.calibrationArrayRight[-self.accuracy:]) / self.accuracy #averages last x elements of right array
            calibrationData['left'][averageSpeedLeft] = leftStage
            calibrationData['right'][-averageSpeedRight] = rightStage
            print('Average speed left: ' + str(averageSpeedLeft))
            print('Average speed right: ' + str(averageSpeedRight))
            #empty everything and reset for next stage
            self.calibrationArrayLeft = []
            self.calibrationArrayRight = []
            self.wheelTicksLeft = 0
            self.wheelTicksRight = 0
            if(leftStage > 1.51 and rightStage < 1.49): #would be miserable going slower than this
                rightStage += 0.0025
                leftStage -= 0.0025
            else:
                rightStage = 1.5
                leftStage = 1.5
        #reset for another run in the opposite direction
        print('CW stage beginning...')
        rightStage = 1.8 #PWM freq for right
        leftStage = 1.2 #PWM freq for left
        while (rightStage > 1.5 and leftStage < 1.5):
            print('Collecting data for (' + str(leftStage) + ', ' + str(rightStage) + ')(1.5, 1.5)...')
            self.setSpeeds(leftStage, rightStage)
            print('Waiting for ticks...')
            while(self.wheelTicksLeft < self.accuracy + 1 and self.wheelTicksRight < self.accuracy + 1): #while loop is just to wait for more ticks
                pass
            print('Got the ticks!')
            averageSpeedLeft = sum(self.calibrationArrayLeft[-self.accuracy:]) / self.accuracy #averages last x elements of left array, left out first because it may not be accurate
            averageSpeedRight = sum(self.calibrationArrayRight[-self.accuracy:]) / self.accuracy #averages last x elements of right array
            calibrationData['left'][-averageSpeedLeft] = leftStage
            calibrationData['right'][averageSpeedRight] = rightStage
            print('Average speed left: ' + str(averageSpeedLeft))
            print('Average speed right: ' + str(averageSpeedRight))
            #empty everything and reset for next stage
            self.calibrationArrayLeft = []
            self.calibrationArrayRight = []
            self.wheelTicksLeft = 0
            self.wheelTicksRight = 0
            if(leftStage < 1.489 and rightStage > 1.511): #would be miserable going slower than this
                rightStage -= 0.0025
                leftStage += 0.0025
            else:
                rightStage = 1.5
                leftStage = 1.5
        print('Turning off servos.')
        self.stopServos()
        #write to file
        with open('calibration.json', 'w') as writeFile:
            json.dump(calibrationData, writeFile, indent=4, separators=(',',': '), sort_keys=True)
        self.calibrating = False
        self.wheelTicksLeft = 0
        self.wheelTicksRight = 0

