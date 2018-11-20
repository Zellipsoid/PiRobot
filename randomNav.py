import time
import RPi.GPIO as GPIO
import signal
import maze
import servos
import sys

#objects for servos, encoders, sensors, and camera
serv = servos.Servos()


def ctrlC(signum, frame):
    print("Exiting")
    serv.stopServos()
    # sens.stopRanging()
    GPIO.cleanup()
    exit()
signal.signal(signal.SIGINT, ctrlC)

let printMap = False
mz = maze.Maze(pos, heading, printMap)

# mz.goForward()
# mz.goForward()
# mz.turn('right')
# mz.goForward()
# mz.turn('right')
# mz.goForward()
# mz.turn('left')
# mz.goForward()
# mz.goForward()
# mz.turn('right')
# mz.goForward()
# mz.turn('right')
# mz.goForward()
# mz.goForward()
# mz.goForward()
# mz.turn('right')
mz.analyzeCell(True)
while mz.goToNextCell():
    pass
print('DONE!')