import encoders
import servos
import time
import RPi.GPIO as GPIO
import signal
import math
import sys

#objects for servos, encoders, sensors, and camera
enc = encoders.Encoders()
serv = servos.Servos()

def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    GPIO.cleanup()
    exit()

signal.signal(signal.SIGINT, ctrlC)

def straightenPath(desiredSpeedLeft, desiredSpeedRight):
    ratio = desiredSpeedLeft / desiredSpeedRight
    ticks = enc.getCounts()
    if (ticks[1] != 0):
        actualRatio = ticks[0] / ticks[1]
    else:
        actualRatio = 1
    percentError = (actualRatio / ratio - 1) * 100
    if percentError > 1.5:
        # print("Slowing left wheel")
        differential = desiredSpeedRight * 0.5
        serv.setSpeedsIPS(desiredSpeedLeft - differential, desiredSpeedRight + differential)
    elif percentError < -1.5:
        # print("Slowing right wheel")
        differential = desiredSpeedLeft * 0.5
        serv.setSpeedsIPS(desiredSpeedLeft + differential, desiredSpeedRight - differential)
    else:
        serv.setSpeedsIPS(desiredSpeedLeft, desiredSpeedRight)

#check for problems and set variables
if len(sys.argv) != 3:
    sys.exit('Error: forward.py requires 2 arguments: distance (in), time (s)')
try:
    targetTime = float(sys.argv[2])
    distance = float(sys.argv[1])
except ValueError:
    sys.exit('Error: arguments must be numbers: distance (in), time (s)')
inchesPerSecond = distance / targetTime
if distance > 0 and serv.getMaxIPS() < inchesPerSecond:
    sys.exit("Error: requested speed exceeds maximum servo output")
elif distance < 0 and serv.getMinIPS() > inchesPerSecond:
    sys.exit("Error: requested speed exceeds maximum servo output")
#press enter to go
go = False
while not go:
    hasInput = input("Press enter to go!")
    if hasInput == '':
        go = True
#set speed and track distance
print("Setting speed to " + str(inchesPerSecond) + " inches/second")
enc.resetCounts()
enc.resetTime()
serv.setSpeedsIPS(inchesPerSecond, inchesPerSecond)
while sum(enc.getDistanceTraveledIPS()) / 2 < abs(distance):
    time.sleep(0.0025) #avoid setting speeds too much
    straightenPath(inchesPerSecond, inchesPerSecond)
serv.stopServos()
distanceTraveled = enc.getDistanceTraveledIPS()
print("Total distance traveled: " + str(sum(distanceTraveled) / 2) + " inches")
print("Total elapsed time: " + str(enc.getElapsedTime()) + " seconds")
print("Average speed: " + str(sum(distanceTraveled) / 2 / enc.getElapsedTime()) + " inches/second")
if (distanceTraveled[0] > distanceTraveled[1]):
    print("Left wheel traveled " + str((distanceTraveled[0] / distanceTraveled[1] - 1) * 100) + "% more than right wheel")
elif(distanceTraveled[1] > distanceTraveled[0]):
    print("Right wheel traveled " + str((distanceTraveled[1] / distanceTraveled[0] - 1) * 100) + "% more than left wheel")
else:
    print("Both wheels traveled the exact same distance!")
