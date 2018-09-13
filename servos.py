import time
import Adafruit_PCA9685
import signal
import math
import encoders
import json

class Servos(object):

    def __init__(self):
        # Initialize the servo hat library.
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(50)
        self.LSERVO = 0
        self.RSERVO = 1
        self.calibrating = false
        self.wheelTicksLeft = 0
        self.wheelTicksRight = 0
        self.calibrationArrayRight = [] #these two arrays hold values for speed that will be averages for each speed increment and put into the json
        self.calibrationArrayLeft = []
        self.encForCal = encoders.Encoders() #encoder object

    def stopServos(self):
        self.pwm.set_pwm(self.LSERVO, 0, 0)
        self.pwm.set_pwm(self.RSERVO, 0, 0)

    def setSpeeds(self, left, right):
        # print("left: " + str(left))
        # print("right: " + str(right))
        self.pwm.set_pwm(self.LSERVO, 0, math.floor(left / 20 * 4096))
        self.pwm.set_pwm(self.RSERVO, 0, math.floor((3 - right) / 20 * 4096))

    #all of this is for calibration
    def leftTick(self):
        if (self.calibrating):
            self.wheelTicksLeft += 1
            self.calibrationArrayLeft.append(self.encForCal.getSpeeds()[0]) #append current left speed to array

    def rightTick(self):
        if (self.calibrating):
            self.wheelTicksRight += 1
            self.calibrationArrayRight.append(self.encForCal.getSpeeds()[1]) #append current right speed to array

    def calibrateSpeeds(self):
        print('Starting calibration...')
        calibrationData = {} #dictionary containing calibration data
        calibrationData['left'] = {}
        calibrationData['right'] = {}
        rightStage = 1.2 #PWM freq for right
        leftStage = 1.8 #PWM freq for left
        print('CCW stage beginning...')
        while (rightStage < 1.5 and leftStage > 1.5):
            print('Collecting data for (' + str(leftStage) + ', ' + str(rightStage) + ')...')
            encForCal.setSpeeds(leftStage, rightStage)
            while(self.wheelTicksLeft < 5 and self.wheelTicksRight < 5): #while loop is just to wait for more ticks
                pass
            averageSpeedLeft = sum(self.calibrationArrayLeft[-4:]) / 4 #averages last 4 elements of left array, left out first because it may not be accurate
            averageSpeedRight = sum(self.calibrationArrayRight[-4:]) / 4 #averages last 4 elements of right array
            calibrationData['left'].append(averageSpeedLeft:leftStage)
            calibrationData['right'].append(averageSpeedRight:rightStage)
            print('Average speed left: ' + str(averageSpeedLeft))
            print('Average speed right: ' + str(averageSpeedRight))
            #empty everything and reset for next stage
            self.calibrationArrayLeft = []
            self.calibrationArrayRight = []
            self.wheelTicksLeft = 0
            self.wheelTicksRight = 0
            if (leftStage > 1.6 and rightStage < 1.4):
                rightStage += 0.01
                leftStage -= 0.01
            elif(leftStage > 1.505 and rightStage < 1.495): #would be miserable going slower than this
                rightStage += 0.005
                leftStage -= 0.005
            else:
                rightStage = 1.5
                leftStage = 1.5
        #reset for another run in the opposite direction
        print('CW stage beginning...')
        rightStage = 1.8 #PWM freq for right
        leftStage = 1.2 #PWM freq for left
        while (rightStage > 1.5 and leftStage < 1.5):
            print('Collecting data for (' + str(leftStage) + ', ' + str(rightStage) + ')...')
            encForCal.setSpeeds(leftStage, rightStage)
            while(self.wheelTicksLeft < 5 and self.wheelTicksRight < 5): #while loop is just to wait for more ticks
                pass
            averageSpeedLeft = sum(self.calibrationArrayLeft[-4:]) / 4 #averages last 4 elements of left array, left out first because it may not be accurate
            averageSpeedRight = sum(self.calibrationArrayRight[-4:]) / 4 #averages last 4 elements of right array
            calibrationData['left'].append(averageSpeedLeft:leftStage)
            calibrationData['right'].append(averageSpeedRight:rightStage)
            print('Average speed left: ' + str(averageSpeedLeft))
            print('Average speed right: ' + str(averageSpeedRight))
            #empty everything and reset for next stage
            self.calibrationArrayLeft = []
            self.calibrationArrayRight = []
            self.wheelTicksLeft = 0
            self.wheelTicksRight = 0
            if (leftStage < 1.4 and rightStage > 1.6):
                rightStage -= 0.01
                leftStage += 0.01
            elif(leftStage < 1.495 and rightStage > 1.505): #would be miserable going slower than this
                rightStage -= 0.005
                leftStage += 0.005
            else:
                rightStage = 1.5
                leftStage = 1.5
        #write to file
        with open('calibration.json', 'w') as writeFile:
            json.dump(calibrationData, writeFile)




# def setSpeedsRPS(rpsLeft, rpsRight):

# def setSpeedsvw(v, w):
