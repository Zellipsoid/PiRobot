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
if len(sys.argv) != 3:
    sys.exit('Error: forward.py requires 2 arguments: distance (in), time (s)')
try:
    time = float(sys.argv[2])
    distance = float(sys.argv[1])
except ValueError:
    sys.exit('Error: arguments must be numbers: distance (in), time (s)')
inchesPerSecond = distance / time
if serv.getMaxIPS() < inchesPerSecond:
    sys.exit("Error: requested speed exceeds maximum servo output")

#set speed and track distance
print("Setting speed to " + str(inchesPerSecond) + " inches/second")
enc.resetCounts()
enc.resetTime()
serv.setSpeedsIPS(inchesPerSecond, inchesPerSecond)
while sum(enc.getDistanceTraveledIPS()) / 2 < distance:
    pass
serv.stopServos()
print("Total distance traveled: " + str(sum(enc.getDistanceTraveledIPS()) / 2) + " inches")
print("Total elapsed time: " + str(enc.getElapsedTime()) + " seconds")
print("Average speed: " + str(sum(enc.getDistanceTraveledIPS()) / 2 / enc.getElapsedTime()) + " inches/second")