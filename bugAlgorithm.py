# This program demonstrates usage of the digital encoders.
# After executing the program, manually spin the wheels and observe the output.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/ for more details.
import servos
import camera
import time
import RPi.GPIO as GPIO
import signal
import bugHelpers

#objects for servos, encoders, sensors, and camera
serv = servos.Servos()
cam = camera.Camera()
bug = bugHelpers.bugHelpers()
wallFollowing = False
def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    GPIO.cleanup()
    exit()
signal.signal(signal.SIGINT, ctrlC)

while True:
    stats = cam.getBlobStats()
    centered = bug.isGoalCentered(stats)
    if (bug.isGoalImmediatelyAhead(stats) and bug.isObstacleAhead()):
        print('in front of goal')
        serv.stopServos()
    if bug.isObstacleAhead() or wallFollowing:
        print('bugging')
        if bug.isObstacleAhead() or not bug.isGoalCentered(stats):
            bug.wallFollow(stats, "right")
            wallFollowing = True
        else:
            wallFollowing = False
    elif not centered:
        print('not centered')
        bug.faceGoal(stats)
    else:
        print('going straight')
        bug.motionToGoal(stats)
    