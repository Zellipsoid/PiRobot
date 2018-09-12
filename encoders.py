import time
import Adafruit_PCA9685
import signal
import math
import pprint


class Encoders(object):

    def __init__(self):
        self.velArrayRight = []
        self.velArrayLeft = []
        self.rightTicks = 0
        self.leftTicks = 0
        self.startTime = time.time()
        self.speedRecord = 2 #number of values to record in record of speed. Min val is 2. Bigger values are less instantaneous but more reliable.
        self.notMovingTimeout = 1 # time in s before declared as not moving if no encoders ticked. The smaller the value, the less accurate but the higher the response time.

    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self, pin):
        #print(self.getCounts() + "left, right ticks")
        self.leftTicks += 1
        self.velArrayLeft.append((time.time(), self.leftTicks))
        if (len(self.velArrayLeft) > self.speedRecord):
            self.velArrayLeft = self.velArrayLeft[1:(self.speedRecord + 1)]

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        #print(self.getCounts() + "left, right ticks")
        self.rightTicks += 1
        self.velArrayRight.append((time.time(), self.rightTicks))
        if (len(self.velArrayRight) > self.speedRecord):
            self.velArrayRight = self.velArrayRight[1:(self.speedRecord + 1)]

    def resetCounts(self):
        self.rightTicks = 0
        self.leftTicks = 0
        self.startTime = time.time() #reseting the ticks also resets the clock time

    def getCounts(self):
        return (self.leftTicks, self.rightTicks)

    def getSpeeds(self):
        totalTime = self.getElapsedTime()
        moving = self.isSpeedZero()
        #pprint(self.velArrayLeft)
        #pprint(self.velArrayRight)
        leftLength = len(self.velArrayLeft)
        rightLength = len(self.velArrayRight)
        # return(
        # (velArrayLeft[1][leftLength - 1] - velArrayLeft[1][leftLength - 2]) / (velArrayLeft[0][leftLength - 1] - velArrayLeft[0][leftLength - 2]),
        # (velArrayRight[1][rightLength - 1] - velArrayRight[1][rightLength - 2]) / (velArrayRight[0][rightLength - 1] - velArrayRight[0][rightLength - 2]))
        if moving[0] == 0 and moving[1] == 0:
            self.resetCounts
        if rightLength > 0 and leftLength > 0 and totalTime > 0:
            # I think all of this was wrong
            # self.totalTimeLeft = 0
            # self.totalTicksLeft = 0
            # for (time, ticks) in self.velArrayLeft:
            #     self.totalTimeLeft += time
            #     self.totalTicksLeft += ticks 
            #     #print(val)
            # self.totalTimeRight = 0
            # self.totalTicksRight = 0
            # for (time, ticks) in self.velArrayRight:
            #     self.totalTimeRight += time
            #     self.totalTicksRight += ticks
            #     #print(val)
            speedLeft = (self.velArrayLeft[leftLength - 1][1] - self.velArrayLeft[0][1]) / (self.velArrayLeft[leftLength - 1][0] - self.velArrayLeft[0][0])
            speedRight = (self.velArrayRight[rightLength - 1][1] - self.velArrayRight[0][1]) / (self.velArrayRight[rightLength - 1][0] - self.velArrayRight[0][0])
            # return (self.totalTicksLeft / totalTime / 32 * moving[0], self.totalTicksRight / totalTime / 32 * moving[1])
            return (speedLeft / 32 * moving[0], speedRight / 32 * moving[1])
        #are these necessary if one wheel is at zero?
        #elif rightLength > 0 and totalTime > 0:
            #speedRight = (self.velArrayRight[rightLength - 1][1] - self.velArrayRight[0][1]) / (self.velArrayRight[rightLength - 1][0] - self.velArrayRight[0][0])
            #return (0, speedRight / 32 * moving[1])
        #elif leftLength > 0 and totalTime > 0:
            #speedLeft = (self.velArrayLeft[leftLength - 1][1] - self.velArrayLeft[0][1]) / (self.velArrayLeft[leftLength - 1][0] - self.velArrayLeft[0][0])
            #return (speedLeft / 32 * moving[0], 0)
        #else:
            #return (0, 0)
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
        #print((timeSinceLeft, timeSinceRight))
            
        if timeSinceRight > self.notMovingTimeout:
            rightMoving = 0
        if timeSinceLeft > self.notMovingTimeout:
            leftMoving = 0
        return (leftMoving, rightMoving)
