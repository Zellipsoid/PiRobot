import time
import Adafruit_PCA9685
import signal
import math

def ctrlC(signum, frame):
    print("Exiting")
    
    # Stop the servos
    pwm.set_pwm(LSERVO, 0, 0)
    pwm.set_pwm(RSERVO, 0, 0)
    
    exit()

def setSpeeds():


def calibrateSpeeds():

def setSpeedsRPS(rpsLeft, rpsRight):

def setSpeedsvw(v, w):
