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
# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18

def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    GPIO.cleanup()
    exit()

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
# Set the pin numbering scheme to the numbering shown on the robot itself.
GPIO.setmode(GPIO.BCM)

# Set encoder pins as input
# Also enable pull-up resistors on the encoder pins
# This ensures a clean 0V and 3.3V is always outputted from the encoders.
GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Attach a rising edge interrupt to the encoder pins
GPIO.add_event_detect(LENCODER, GPIO.RISING, enc.onLeftEncode)
GPIO.add_event_detect(RENCODER, GPIO.RISING, enc.onRightEncode)

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
