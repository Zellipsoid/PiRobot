# This program demonstrates usage of the digital encoders.
# After executing the program, manually spin the wheels and observe the output.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/ for more details.
import encoders
import servos
import sensors
import camera
import time
import RPi.GPIO as GPIO
import signal
import bugHelpers

#objects for servos, encoders, sensors, and camera
enc = encoders.Encoders()
serv = servos.Servos()
cam = camera.Camera()
bug = bugHelpers.bugHelpers()

def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    GPIO.cleanup()
    exit()
signal.signal(signal.SIGINT, ctrlC)

while True:
    stats = cam.getBlobStats()
    centered = bug.isGoalCentered(stats)
    if not centered:
        print('not centered')
        bug.faceGoal(stats)
    elif (centered and bug.isObstacleAhead()):
        print('in front of goal')
        serv.stopServos()
    else:
        print('going straight')
        bug.motionToGoal(stats)
    