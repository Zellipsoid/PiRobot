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
# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, enc.ctrlC)

def correctPath(desiredSpeedLeft, desiredSpeedRight):
    ratio = desiredSpeedLeft / desiredSpeedRight
    ticks = enc.getCounts()
    if (ticks[1] != 0):
        actualRatio = ticks[0] / ticks[1]
    else:
        actualRatio = ratio
    percentError = (actualRatio / ratio - 1) * 100
    # print(percentError)
    if percentError > 0.75:
        # print("Slowing left wheel")
        # differential = desiredSpeedRight * 0.5
        # serv.setSpeedsIPS(desiredSpeedLeft - differential, desiredSpeedRight + differential)
        serv.setSpeedsIPS(desiredSpeedLeft * 0.7, desiredSpeedRight *1.25)
    elif percentError < -0.75:
        # print("Slowing right wheel")
        # differential = desiredSpeedLeft * 0.5
        # serv.setSpeedsIPS(desiredSpeedLeft + differential, desiredSpeedRight - differential)
        serv.setSpeedsIPS(desiredSpeedLeft * 1.25, desiredSpeedRight * 0.7)
    else:
        serv.setSpeedsIPS(desiredSpeedLeft, desiredSpeedRight)

#check for problems and set variables
if len(sys.argv) != 3:
    sys.exit('Error: circle.py requires 3 arguments: Radius1 (in), time (s)')
try:
    R1 = float(sys.argv[1])
    targetTime = float(sys.argv[2])
except ValueError:
    sys.exit('Error: arguments must be numbers: Radius1 (in), time (s)')
distance = math.pi * abs(R1)
outerDistance = math.pi * (abs(R1) + serv.getDistanceBetweenWheels() / 2) # max distance servo must travel
velocity = distance / targetTime #speed needed to travel to meet requirements
outerVelocity = outerDistance / targetTime # max velocity for outside wheel
omega = velocity / R1 #negative because first circle is clockwise 
if serv.getMaxIPS() < outerVelocity:
    sys.exit("Error: requested speed exceeds maximum servo output")

#first stage
go = False
while not go:
    hasInput = input("Press enter to start first semicircle!")
    if hasInput == '':
        go = True
#set speed and track distance
print('Ratio should be ' + str((abs(R1) + serv.getDistanceBetweenWheels() / 2) / (abs(R1) - serv.getDistanceBetweenWheels() / 2)))
print("Setting speed to " + str(velocity) + " inches/second and angular velocity to " + str(omega) + " radians/second")
enc.resetCounts()
enc.resetTime()
desiredSpeedTuple = serv.setSpeedsVW(velocity, omega * 1.05) #get correct ratio of wheel speed; increase omega to account for friction
while sum(enc.getDistanceTraveledIPS()) / 2 < distance:
    time.sleep(0.0025)
    correctPath(desiredSpeedTuple[0], desiredSpeedTuple[1])
serv.stopServos()
distanceTraveled = enc.getDistanceTraveledIPS()
elapsedTime = enc.getElapsedTime()
# print(distanceTraveled)
print("First semicircle finished, pausing")
print("Total distance traveled for this arc: " + str(sum(distanceTraveled) / 2) + " inches")
print("Total elapsed time for this arc: " + str(elapsedTime) + " seconds")
print("Average speed for this arc: " + str(sum(distanceTraveled) / 2 / elapsedTime) + " inches/second")
print('Ratio is ' + str(distanceTraveled[1] / distanceTraveled[0]))
