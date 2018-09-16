import encoders
import servos
import time
import RPi.GPIO as GPIO
import signal
import math

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

distance1 = 0
distance2 = 0
speedTuple = enc.getSpeeds()
timeSince = enc.getElapsedTime()

inches = input("Please input X (in inches) ")
seconds = input("Please input Y (in seconds) ")
speed = float(float(inches)/float(seconds))

while True:
    time.sleep(1)
    serv.setSpeedsIPS(speed, speed)
    timeSince += timeSince
    distance1 += (speedTuple[0] * 2.61 * math.pi) * timeSince 
    #calculates distance traveled based on RPS to IPS multiplied by time elapsed
    distance2 += (speedTuple[1] * 2.61 * math.pi) * timeSince 

    print(distance1)
    print(distance2)
    print(timeSince)

    if distance1 >= float(inches) or distance2 >= float(inches):
      print("roboto stopped")
      serv.setSpeedsIPS(0,0)
        
    if timeSince > float(seconds):
      print("roboto stopped")
      serv.setSpeedsIPS(0,0)
    
    print(enc.getSpeeds())
