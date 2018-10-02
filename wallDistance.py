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
def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    sens.stopRanging()
    GPIO.cleanup()
    exit()

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
        if (ticks[0] > 50 or ticks[1] > 50):
            enc.subtractCounts(25)

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)

goalInches = 5
constantKp = 1.5
# StopMovingMarginOfError = 0.1 # stop moving when in this range
# StartMovingMarginOfError = 0.2 # start moving when out of this range
# moving = True

while True:
    difference = goalInches - sens.getProxForwardInches()
    newOutput =  -constantKp * difference #* difference
    # print(abs(difference))
    # print(enc.getSpeeds())
    # if abs(difference) > StopMovingMarginOfError and moving:
    #     moving = True
    serv.setSpeedsIPS(newOutput, newOutput)
    time.sleep(0.0025)
        # serv.setSpeedsIPS(newOutput, newOutput)
    # straightenPath(newOutput, newOutput)
    # elif abs(difference) <= StopMovingMarginOfError:
    #     moving = False
    #     serv.stopServos()
    # elif not moving and abs(difference) > StartMovingMarginOfError:
    #     moving = True
