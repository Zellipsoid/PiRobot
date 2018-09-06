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
        self.speedRecord = 10

    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self, pin):
        print("Left encoder ticked!")
        self.leftTicks += 1
        self.velArrayLeft.append((time.time(), self.leftTicks))
        if (len(self.velArrayLeft) > self.speedRecord):
            self.velArrayLeft = self.velArrayLeft[1:(self.speedRecord + 1)]

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        print("Right encoder ticked!")
        self.rightTicks += 1
        self.velArrayRight.append((time.time(), self.rightTicks))
        if (len(self.velArrayRight) > self.speedRecord):
            self.velArrayRight = self.velArrayRight[1:(self.speedRecord + 1)]

    def resetCounts(self):
        self.rightTicks = 0
        self.leftTicks = 0

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
            speedLeft = (velArrayLeft[1][leftLength] - velArrayLeft[1][0]) / (velArrayLeft[0][leftLength] - velArrayLeft[0][0])
            speedRight = (velArrayRight[1][rightLength] - velArrayRight[1][0]) / (velArrayRight[0][rightLength] - velArrayRight[0][0])
            # return (self.totalTicksLeft / totalTime / 32 * moving[0], self.totalTicksRight / totalTime / 32 * moving[1])
            return (speedLeft * moving[0], speedRight * moving[1])
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
        print((timeSinceLeft, timeSinceRight))
            
        if timeSinceRight > 1.5:
            rightMoving = 0
        if timeSinceLeft > 1.5:
            leftMoving = 0
        return (leftMoving, rightMoving)
