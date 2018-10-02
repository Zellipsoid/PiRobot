# This program demonstrates usage of the digital encoders.
# After executing the program, manually spin the wheels and observe the output.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/ for more details.
import encoders
import servos
import sensors
import time
import RPi.GPIO as GPIO
import signal
import xlsxwriter as xl

#objects for servos, encoders, sensors, and camera
enc = encoders.Encoders()
serv = servos.Servos()
sens = sensors.Sensors()
def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    sens.stopRanging()
    GPIO.cleanup()
    #if workbook:
    #    workbook.close()
    exit()

# def straightenPath(desiredSpeedLeft, desiredSpeedRight):
#     ratio = desiredSpeedLeft / desiredSpeedRight
#     ticks = enc.getCounts()
#     if (ticks[1] != 0):
#         actualRatio = ticks[0] / ticks[1]
#     else:
#         actualRatio = 1
#     percentError = (actualRatio / ratio - 1) * 100
#     if percentError > 1.5:
#         # print("Slowing left wheel")
#         differential = desiredSpeedRight * 0.5
#         serv.setSpeedsIPS(desiredSpeedLeft - differential, desiredSpeedRight + differential)
#     elif percentError < -1.5:
#         # print("Slowing right wheel")
#         differential = desiredSpeedLeft * 0.5
#         serv.setSpeedsIPS(desiredSpeedLeft + differential, desiredSpeedRight - differential)
#     else:
#         serv.setSpeedsIPS(desiredSpeedLeft, desiredSpeedRight)
#         if (ticks[0] > 50 or ticks[1] > 50):
#             enc.subtractCounts(25)
# def moveBack():
#     distance = -15
#     targetTime = 8
#     inchesPerSecond = distance / targetTime
#     enc.resetCounts()
#     enc.resetTime()
#     serv.setSpeedsIPS(inchesPerSecond, inchesPerSecond)
#     while sum(enc.getDistanceTraveledIPS()) / 2 < abs(distance):
#         time.sleep(0.0025) #avoid setting speeds too much
#         straightenPath(inchesPerSecond, inchesPerSecond)
#     serv.stopServos()
# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)

goalInches = 5
constantKp = [0.2, 0.6, 0.9, 1.2, 1.5, 2.0, 5.0]

workbook = xl.Workbook('L2C2.xlsx')
worksheet = workbook.add_worksheet()
#print(type(constantKp))
#write headers
for (index, item) in enumerate(constantKp):
    col = index * 2 + 1
    worksheet.write(0, col, item)

for (index, Kp) in enumerate(constantKp):
    #have user move back to 10 inches then press enter
    go = False
    while not go:
        hasInput = input("Press enter to start collecting data for Kp=" + str(Kp))
        if hasInput == '':
            go = True
    print("Working...")
    #reset variables
    enc.resetTime()
    enc.resetCounts()
    #do the test
    distanceVsTime = []
    count = 0
    while enc.getElapsedTime() < 4:
        elapsedTime = enc.getElapsedTime()
        distance = sens.getProxForwardInches()
        # if count % 5 == 0:
        distanceVsTime.append((elapsedTime, distance))
        difference = goalInches - distance
        newOutput =  -Kp * difference
        serv.setSpeedsIPS(newOutput, newOutput)
        count += 1
        time.sleep(0.0025)
    serv.stopServos()
    #graph it
    col = index * 2 + 1
    row = 1
    for item in distanceVsTime:
        worksheet.write(row, col, item[0])
        worksheet.write(row, col + 1, item[1])
        row += 1
    print("Done collecting data for Kp=" + str(Kp))
workbook.close()
sens.stopRanging()
