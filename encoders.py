import time
import Adafruit_PCA9685
import signal
import math
import pprint


velArrayRight = []
velArrayLeft = []
rightTicks = 0
leftTicks = 0
tempRightTicks = 0
tempLeftTicks = 0
startTime = time.time()
#tempStartTime = time.time();

# This function is called when the left encoder detects a rising edge signal.
def onLeftEncode(pin):
    print("Left encoder ticked!")
    leftTicks += 1
    tempLeftTicks += 1
    velArrayLeft.append((time.time(), leftTicks))
    if (len(velArrayLeft) > 5):
        velArrayLeft = velArrayLeft[1:6]

# This function is called when the right encoder detects a rising edge signal.
def onRightEncode(pin):
    print("Right encoder ticked!")
    rightTicks += 1
    tempRightTicks += 1
    velArrayRight.append((time.time(), rightTicks))
    if (len(velArrayRight) > 5):
        velArrayRight = velArrayRight[1:6]

def initEncoders():
    velArrayRight = []
    velArrayLeft = []
    rightTicks = 0
    leftTicks = 0
    tempRightTicks = 0
    tempLeftTicks = 0
    startTime = time.time()

def resetCounts():
    rightTicks = 0
    leftTicks = 0

def resetTempCounts():
    tempRightTicks = 0
    tempLeftTicks = 0

def getCounts():
    return (leftTicks, rightTicks)

def getSpeeds():
    pprint(velArrayLeft)
    pprint(velArrayRight)
    leftLength = len(velArrayLeft)
    rightLength = len(velArrayRight)
    return(
    (velArrayLeft[1][leftLength - 1] - velArrayLeft[1][leftLength - 2]) / (velArrayLeft[0][leftLength - 1] - velArrayLeft[0][leftLength - 2]),
    (velArrayRight[1][rightLength - 1] - velArrayRight[1][rightLength - 2]) / (velArrayRight[0][rightLength - 1] - velArrayRight[0][rightLength - 2]))
    


def getElapsedTime():
    return time.time() - startTime

#while True:
#    time.sleep(0.25)
#    resetCounts()
#    tempStartTime = time.time()

