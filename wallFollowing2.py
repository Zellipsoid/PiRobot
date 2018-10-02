# This program demonstrates usage of the digital encoders.
# After executing the program, manually spin the wheels and observe the output.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/ for more details.
import encoders
import servos
import sensors
import time
import RPi.GPIO as GPIO
import signal

#objects for servos, encoders, sensors, and camera
enc = encoders.Encoders()
serv = servos.Servos()
sens = sensors.Sensors()
goalInches = 5.5
constantKp = 1
turningLinearVel = 0.1
turningAngularVel = 1.5
def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    sens.stopRanging()
    GPIO.cleanup()
    exit()

def wallFollow(side, distance):
    if side == 'left':
        tempKp = -constantKp
    else:
        tempKp = constantKp
    difference = goalInches - distance
    omega =  tempKp * difference
    if omega > 1.5:
        omega = 1.5
    if omega < -1.5:
        omega = -1.5
    print(omega)
    serv.setSpeedsVW(5, omega)
    #AVOID FRONT WALLS
    closeEnoughToLoop = 6
    while sens.getProxForwardInches() < closeEnoughToLoop:
        closeEnoughToLoop = 15
        if (side == 'left'):
            serv.setSpeedsVW(turningLinearVel, -turningAngularVel)
        else:
            serv.setSpeedsVW(turningLinearVel, turningAngularVel)
# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)


# StopMovingMarginOfError = 0.1 # stop moving when in this range
# StartMovingMarginOfError = 0.2 # start moving when out of this range
# moving = True
lastWall = 'right'
while True:
    leftDistance = sens.getProxLeftInches()
    rightDistance = sens.getProxRightInches()
    #if leftDistance > 15 and rightDistance > 15:
    #    serv.setSpeedsVW(5, 0) 
    if (rightDistance < leftDistance and leftDistance < 15):
        lastWall = 'right'
        wallFollow('right', rightDistance)
    elif leftDistance < rightDistance and rightDistance < 15:
        lastWall = 'left'
        wallFollow('left', leftDistance)
    elif lastWall == 'right':
        wallFollow('right', rightDistance)
    else:
        wallFollow('left', leftDistance)
