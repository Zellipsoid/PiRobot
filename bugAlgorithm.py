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

side = "left"
while True:
    stats = cam.getBlobStats()
    centered = bug.isGoalCentered(stats)
    dangerRight = bug.isObstacleToRight()
    dangerLeft = bug.isObstacleToLeft() 
    if (bug.isGoalImmediatelyAhead(stats) and bug.isObstacleAhead()):
        print('in front of goal')
        serv.stopServos()
    if bug.isObstacleAhead() or wallFollowing or dangerRight or dangerLeft:
        print('checking bug')
        if dangerLeft or dangerRight or not bug.isGoalCentered(stats):
            print('bugging')
            if dangerRight:
                side = "right"
            elif dangerLeft:
                side = "left"
            bug.wallFollow(stats, side)
            wallFollowing = True
        else:
            print('ending bug')
            wallFollowing = False
    elif not centered:
        print('not centered')
        bug.faceGoal(stats)
    else:
        print('going straight')
        bug.motionToGoal(stats)
    