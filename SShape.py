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
# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18

def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    GPIO.cleanup()
    exit()

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
# Set the pin numbering scheme to the numbering shown on the robot itself.
GPIO.setmode(GPIO.BCM)

# Set encoder pins as input
# Also enable pull-up resistors on the encoder pins
# This ensures a clean 0V and 3.3V is always outputted from the encoders.
GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Attach a rising edge interrupt to the encoder pins
GPIO.add_event_detect(LENCODER, GPIO.RISING, enc.onLeftEncode)
GPIO.add_event_detect(RENCODER, GPIO.RISING, enc.onRightEncode)

#check for problems and set variables
if len(sys.argv) != 4:
    sys.exit('Error: forward.py requires 3 arguments: Radius1 (in), Radius2 (in), time (s)')
try:
    time = float(sys.argv[3])
    R1 = float(sys.argv[1])
    R2 = float(sys.argv[2])
except ValueError:
    sys.exit('Error: arguments must be numbers: Radius1 (in), Radius2 (in), time (s)')
distance1 = math.pi * R1
distance2 = math.pi * R2
velocity = (distance1 + distance2) / time #speed needed to travel to meet requirements
omega1 = -velocity / R1 #negative because first circle is clockwise
omega2 = velocity / R2 
if serv.getMaxIPS() < velocity:
    sys.exit("Error: requested speed exceeds maximum servo output")

#first stage
go = False
while not go:
    hasInput = input("Press enter to start first semicircle!")
    if hasInput == '':
        go = True
#set speed and track distance
print("Setting speed to " + str(velocity) + " inches/second and angular velocity to " + str(omega1) + " radians/second")
enc.resetCounts()
enc.resetTime()
serv.setSpeedsVW(velocity, omega1)
while sum(enc.getDistanceTraveledIPS()) / 2 < distance1:
    pass
serv.stopServos()
distanceTraveled1 = enc.getDistanceTraveledIPS()
elapsedTime1 = enc.getElapsedTime()
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
print("Setting speed to " + str(velocity) + " inches/second and angular velocity to " + str(omega2) + " radians/second")
enc.resetCounts()
enc.resetTime()
serv.setSpeedsVW(velocity, omega2)
while sum(enc.getDistanceTraveledIPS()) / 2 < distance2:
    pass
serv.stopServos()
distanceTraveled2 = enc.getDistanceTraveledIPS()
elapsedTime2 = enc.getElapsedTime()
print("Second semicircle finished, finishing")
print("Total distance traveled for this arc: " + str(sum(distanceTraveled2) / 2) + " inches")
print("Total elapsed time for this arc: " + str(elapsedTime2) + " seconds")
print("Average speed for this arc: " + str(sum(distanceTraveled2) / 2 / elapsedTime2) + " inches/second")
print("--------------------------------------------------------------------------------")
print("Total distance traveled overall: " + str((sum(distanceTraveled1) + sum(distanceTraveled2)) / 2) + " inches")
print("Total elapsed time overall: " + str(elapsedTime1 + elapsedTime2) + " seconds")
print("Average speed overall: " + str((sum(distanceTraveled1) + sum(distanceTraveled2)) / 2 / (elapsedTime1 + elapsedTime2)) + " inches/second")