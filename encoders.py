import time
import Adafruit_PCA9685
import signal
import math
import pprint


class Encoders(object):

    velArrayRight = []
    velArrayLeft = []
    rightTicks = 0
    leftTicks = 0
    tempRightTicks = 0
    tempLeftTicks = 0
    startTime = time.time()
    #tempStartTime = time.time();

    def __init__(self):
        velArrayRight = []
        velArrayLeft = []
        global rightTicks = 0
        global leftTicks = 0
        tempRightTicks = 0
        tempLeftTicks = 0
        startTime = time.time()

    # This function is called when the left encoder detects a rising edge signal.
    def onLeftEncode(self, pin):
        print("Left encoder ticked!")
        global leftTicks += 1
        tempLeftTicks += 1
        velArrayLeft.append((time.time(), leftTicks))
        if (len(velArrayLeft) > 24):
            velArrayLeft = velArrayLeft[1:25]

    # This function is called when the right encoder detects a rising edge signal.
    def onRightEncode(self, pin):
        print("Right encoder ticked!")
        global rightTicks += 1
        tempRightTicks += 1
        velArrayRight.append((time.time(), rightTicks))
        if (len(velArrayRight) > 24):
            velArrayRight = velArrayRight[1:25]

    def resetCounts(self):
        rightTicks = 0
        leftTicks = 0

    def resetTempCounts(self):
        tempRightTicks = 0
        tempLeftTicks = 0

    def getCounts(self):
        return (leftTicks, rightTicks)

    def getSpeeds(self):
        pprint(velArrayLeft)
        pprint(velArrayRight)
        leftLength = len(velArrayLeft)
        rightLength = len(velArrayRight)
        # return(
        # (velArrayLeft[1][leftLength - 1] - velArrayLeft[1][leftLength - 2]) / (velArrayLeft[0][leftLength - 1] - velArrayLeft[0][leftLength - 2]),
        # (velArrayRight[1][rightLength - 1] - velArrayRight[1][rightLength - 2]) / (velArrayRight[0][rightLength - 1] - velArrayRight[0][rightLength - 2]))
        if rightLength > 0 and leftLength > 0:
            totalTimeLeft = 0
            totalTicksLeft = 0
            for i in velArrayLeft:
                totalTimeLeft += velArrayLeft[0][i]
                totalTicksLeft += velArrayLeft[1][i] 
            totalTimeRight = 0
            totalTicksRight = 0
            for i in velArrayRight:
                totalTimeRight += velArrayRight[0][i]
                totalTicksRight += velArrayRight[1][i]
            return (totalTicksLeft / totalTimeLeft / 32, totalTicksRight / totalTimeRight / 32)
        else:
            return (0, 0)

    def getElapsedTime(self):
        return time.time() - startTime
