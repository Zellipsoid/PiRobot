# This program demonstrates usage of the digital encoders.
# After executing the program, manually spin the wheels and observe the output.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/ for more details.
import encoders
import servos
import time
import RPi.GPIO as GPIO
import signal
import xlsxwriter as xl

#objects for servos, encoders, sensors, and camera
enc = encoders.Encoders()
serv = servos.Servos()

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)

def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    GPIO.cleanup()
    exit()

print('Setting speeds to the MAAAX!!!')
speeds = [] #list to store instantaneous speeds in
serv.setSpeedsRPS(0, 100) #sets speed to max
time.sleep(1) #waits a second for speed to stabilize
enc.resetTime()
while enc.getElapsedTime() <= 10:
    #print(enc.getSpeeds()[1])
    speeds.append((enc.getSpeeds()[1], enc.getElapsedTime()))
    time.sleep(0.03)
serv.stopServos()
workbook = xl.Workbook('C1.xlsx')
worksheet = workbook.add_worksheet()
col = 0
row = 0
for item in speeds:
    worksheet.write(row, col, item[0])
    worksheet.write(row, col + 1, item[1])
    row += 1
workbook.close()
