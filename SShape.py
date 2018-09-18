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

def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    GPIO.cleanup()
    exit()
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
if len(sys.argv) != 4:
    sys.exit('Error: forward.py requires 3 arguments: Radius1 (in), Radius2 (in), time (s)')
try:
    targetTime = float(sys.argv[3])
    R1 = float(sys.argv[1])
    R2 = float(sys.argv[2])
except ValueError:
    sys.exit('Error: arguments must be numbers: Radius1 (in), Radius2 (in), time (s)')
distance1 = math.pi * abs(R1)
distance2 = math.pi * abs(R2)
totalDistance = math.pi * (abs(R1) + abs(R2))
outerDistance1 = math.pi * (abs(R1) + serv.getDistanceBetweenWheels() / 2) # max distance servo must travel
outerDistance2 = math.pi * (abs(R2) + serv.getDistanceBetweenWheels() / 2) # max distance servo must travel
velocity = (distance1 + distance2) / targetTime #speed needed to travel to meet requirements
outerVelocity1 = outerDistance1 / targetTime # max velocity for outside wheel
outerVelocity2 = outerDistance2 / targetTime # max velocity for outside wheel
omega1 = -velocity / R1 #negative because first circle is clockwise 
omega2 = velocity / R2
if serv.getMaxIPS() < outerVelocity1:
    sys.exit("Error: requested speed for arc 1 exceeds maximum servo output")
if serv.getMaxIPS() < outerVelocity2:
    sys.exit("Error: requested speed for arc 2 exceeds maximum servo output")

#first stage
go = False
while not go:
    hasInput = input("Press enter to start first semicircle!")
    if hasInput == '':
        go = True
#set speed and track distance
print('Ratio should be ' + str((abs(R1) + serv.getDistanceBetweenWheels() / 2) / (abs(R1) - serv.getDistanceBetweenWheels() / 2)))
print("Setting speed to " + str(velocity) + " inches/second and angular velocity to " + str(omega1) + " radians/second")
enc.resetCounts()
enc.resetTime()
desiredSpeedTuple = serv.setSpeedsVW(velocity, omega1 * 1.125) #get correct ratio of wheel speed; increase omega to account for friction
while sum(enc.getDistanceTraveledIPS()) / 2 < distance1:
    time.sleep(0.0025) #avoid setting speeds too much
    correctPath(desiredSpeedTuple[0], desiredSpeedTuple[1]) #fixes incorrect paths
serv.stopServos()
distanceTraveled1 = enc.getDistanceTraveledIPS()
elapsedTime1 = enc.getElapsedTime()
# print(distanceTraveled)
print("First semicircle finished, pausing")
print("Total distance traveled for this arc: " + str(sum(distanceTraveled1) / 2) + " inches")
print("Total elapsed time for this arc: " + str(elapsedTime1) + " seconds")
print("Average speed for this arc: " + str(sum(distanceTraveled1) / 2 / elapsedTime1) + " inches/second")

#second stage
go = False
while not go:
    hasInput = input("Press enter to start second semicircle!")
    if hasInput == '':
        go = True
#set speed and track distance
print('Ratio should be ' + str((abs(R2) + serv.getDistanceBetweenWheels() / 2) / (abs(R2) - serv.getDistanceBetweenWheels() / 2)))
print("Setting speed to " + str(velocity) + " inches/second and angular velocity to " + str(omega2) + " radians/second")
enc.resetCounts()
enc.resetTime()
desiredSpeedTuple = serv.setSpeedsVW(velocity, omega2 * 1.125) #get correct ratio of wheel speed; increase omega to account for friction
while sum(enc.getDistanceTraveledIPS()) / 2 < distance2:
    time.sleep(0.0025) #avoid setting speeds too much
    correctPath(desiredSpeedTuple[0], desiredSpeedTuple[1]) #fixes incorrect paths
serv.stopServos()
distanceTraveled2 = enc.getDistanceTraveledIPS()
elapsedTime2 = enc.getElapsedTime()
# print(distanceTraveled)
print("Second semicircle finished, ending")
print("Total distance traveled for this arc: " + str(sum(distanceTraveled2) / 2) + " inches")
print("Total elapsed time for this arc: " + str(elapsedTime2) + " seconds")
print("Average speed for this arc: " + str(sum(distanceTraveled2) / 2 / elapsedTime2) + " inches/second")


print("--------------------------------------------------------------------------------")
print("Total distance traveled overall: " + str((sum(distanceTraveled1) + sum(distanceTraveled2)) / 2) + " inches")
print("Total elapsed time overall (excluding pause): " + str(elapsedTime1 + elapsedTime2) + " seconds")
print("Average speed overall (excluding pause): " + str((sum(distanceTraveled1) + sum(distanceTraveled2)) / 2 / (elapsedTime1 + elapsedTime2)) + " inches/second")