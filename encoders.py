import time
import Adafruit_PCA9685
import signal
import math
import pprint


class Encoders(object):

    # velArrayRight = []
    # velArrayLeft = []
    # rightTicks = 0
    # leftTicks = 0
    # tempRightTicks = 0
    # tempLeftTicks = 0
    # startTime = time.time()
    # #tempStartTime = time.time();

    def __init__(self):
        self.velArrayRight = []
        self.velArrayLeft = []
        self.rightTicks = 0
        self.leftTicks = 0
        self.tempRightTicks = 0
        self.tempLeftTicks = 0
        self.startTime = time.time()

    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self, pin):
        print("Left encoder ticked!")
        self.leftTicks 
        self.leftTicks += 1
        self.tempLeftTicks += 1
        self.velArrayLeft.append((time.time(), self.leftTicks))
        if (len(self.velArrayLeft) > 24):
            self.velArrayLeft = self.velArrayLeft[1:25]

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        print("Right encoder ticked!")
        self.rightTicks 
        self.rightTicks += 1
        self.tempRightTicks += 1
        self.velArrayRight.append((time.time(), self.rightTicks))
        if (len(self.velArrayRight) > 24):
            self.velArrayRight = self.velArrayRight[1:25]

    def resetCounts(self):
        self.rightTicks = 0
        self.leftTicks = 0

    def resetTempCounts(self):
        self.tempRightTicks = 0
        self.tempLeftTicks = 0

    def getCounts(self):
        return (self.leftTicks, self.rightTicks)

    def getSpeeds(self):
        totalTime = self.getElapsedTime()
        #pprint(self.velArrayLeft)
        #pprint(self.velArrayRight)
        leftLength = len(self.velArrayLeft)
        rightLength = len(self.velArrayRight)
        # return(
        # (velArrayLeft[1][leftLength - 1] - velArrayLeft[1][leftLength - 2]) / (velArrayLeft[0][leftLength - 1] - velArrayLeft[0][leftLength - 2]),
        # (velArrayRight[1][rightLength - 1] - velArrayRight[1][rightLength - 2]) / (velArrayRight[0][rightLength - 1] - velArrayRight[0][rightLength - 2]))
        if rightLength > 0 and leftLength > 0 and totalTime > 0:
            self.totalTimeLeft = 0
            self.totalTicksLeft = 0
            for (time, ticks) in self.velArrayLeft:
                self.totalTimeLeft += time
                self.totalTicksLeft += ticks 
                #print(val)
            self.totalTimeRight = 0
            self.totalTicksRight = 0
            for (time, ticks) in self.velArrayRight:
                self.totalTimeRight += time
                self.totalTicksRight += ticks
                #print(val)
            return (self.totalTicksLeft / totalTime / 32, self.totalTicksRight / totalTime / 32)
        else:
            return (0, 0)

    def getElapsedTime(self):
        return time.time() - self.startTime
