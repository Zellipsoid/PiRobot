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
        velArrayRight = []
        velArrayLeft = []
        rightTicks = 0
        leftTicks = 0
        tempRightTicks = 0
        tempLeftTicks = 0
        startTime = time.time()

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
        pprint(self.velArrayLeft)
        pprint(self.velArrayRight)
        leftLength = len(self.velArrayLeft)
        rightLength = len(self.velArrayRight)
        # return(
        # (velArrayLeft[1][leftLength - 1] - velArrayLeft[1][leftLength - 2]) / (velArrayLeft[0][leftLength - 1] - velArrayLeft[0][leftLength - 2]),
        # (velArrayRight[1][rightLength - 1] - velArrayRight[1][rightLength - 2]) / (velArrayRight[0][rightLength - 1] - velArrayRight[0][rightLength - 2]))
        if rightLength > 0 and leftLength > 0:
            self.totalTimeLeft = 0
            self.totalTicksLeft = 0
            for i in self.velArrayLeft:
                self.totalTimeLeft += self.velArrayLeft[0][i]
                self.totalTicksLeft += self.velArrayLeft[1][i] 
            self.totalTimeRight = 0
            self.totalTicksRight = 0
            for i in self.velArrayRight:
                self.totalTimeRight += self.velArrayRight[0][i]
                self.totalTicksRight += self.velArrayRight[1][i]
            return (self.totalTicksLeft / self.totalTimeLeft / 32, self.totalTicksRight / self.totalTimeRight / 32)
        else:
            return (0, 0)

    def getElapsedTime(self):
        return time.time() - self.startTime
