import encoders
import servos
import sensors
import time
import math


class bugHelpers(object):
    def __init__(self):
        self.serv = servos.Servos()
        self.sens = sensors.Sensors()
        self.enc = encoders.Encoders()
        self.lastSeenGoalDirection = 'right'
        self.forwardDistanceThreshold = 6
        self.speed = 4

    def faceGoal(self, blobStats):
        #self.serv.stopServos()
        Kp = 0.004
        if blobStats['blobs'] == False:
            print('Searching...')
            if self.lastSeenGoalDirection == 'right': 
                self.serv.setSpeedsVW(0, -Kp * 320)
            else:
                self.serv.setSpeedsVW(0, Kp * 320)
        else:
            if blobStats['averageX'] > 320:
                self.lastSeenGoalDirection = 'right'
            else:
                self.lastSeenGoalDirection = 'left'
            error = 320 - blobStats['averageX']
            if (abs(error) < 45 or abs(blobStats['leftmost'] - blobStats['rightmost']) > 150):
                print('Success!')
                self.serv.stopServos()
                print(error)
                return
            self.serv.setSpeedsVW(0, error * Kp)
            print(error * Kp)  

    def isGoalCentered(self, blobStats):
        if blobStats['blobs'] == False:
            return False
        else:
            error = 320 - blobStats['averageX']
            if (abs(error) < 135 or abs(blobStats['leftmost'] - blobStats['rightmost']) > 150): #worked pretty well at 135, 150
                return True
            else:
                return False

    def motionToGoal(self, blobStats):
        Kp = 0.003
        if blobStats['blobs'] == False:
            return 1
        else:
            omega = Kp * (320 - blobStats['averageX'])
            self.serv.setSpeedsVW(self.speed, omega)
    def isGoalImmediatelyAhead(self, blobStats):
        if blobStats['maxDiameter'] > 450:
            return True
        else:
            return False
    def isObstacleAhead(self):
        if self.sens.getProxForwardInches() < self.forwardDistanceThreshold:
            return True
        else:
            return False

    def wallFollow(self, blobStats, side):
        goalInches = 5
        constantKp = 1
        turningLinearVel = 0.1
        turningAngularVel = 1.5
    
        #AVOID FRONT WALLS
        closeEnoughToLoop = 6
        # while self.sens.getProxForwardInches() < closeEnoughToLoop:
        #     closeEnoughToLoop = 14
        #     if (side == 'left'):
        #         self.serv.setSpeedsVW(turningLinearVel, -turningAngularVel)
        #     else:
        #         self.serv.setSpeedsVW(turningLinearVel, turningAngularVel)
        
        if self.sens.getProxForwardInches() < closeEnoughToLoop:
            breakLoopFront = 14
            breakLoopSide = 6
            sideDistance = breakLoopSide + 1
            self.enc.resetCounts() #resets counts of wheels. Keeps count, if robot turns more than 120 degrees, breaks loop
            while ((self.sens.getProxForwardInches() < breakLoopFront or sideDistance > breakLoopSide) and self.enc.getDistanceTraveledIPS()[0] < self.enc.getWheelsDiameter() * math.pi / 3): #breaks loop if turns more than a third of circle
                if (side == 'left'):                    
                    self.serv.setSpeedsVW(turningLinearVel, -turningAngularVel)
                    sideDistance = self.sens.getProxLeftInches()
                else:
                    self.serv.setSpeedsVW(turningLinearVel, turningAngularVel)
                    sideDistance = self.sens.getProxRightInches()
        if side == 'left':
            tempKp = -constantKp
            distance = self.sens.getProxLeftInches()
        else:
            tempKp = constantKp
            distance = self.sens.getProxRightInches()
        difference = goalInches - distance
        omega =  tempKp * difference
        if omega > 1.5:
            omega = 1.5
        if omega < -1.5:
            omega = -1.5
        #print(distance)
        self.serv.setSpeedsVW(self.speed, omega)
        return
