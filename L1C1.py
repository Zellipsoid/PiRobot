
import time
import "PiRobot/Sample+Code/4_ServoSetup/servos.py"

setSpeeds(0,100) # linear speed, angular velocity

time.sleep(1)

start_time = time.time()
elapsed_time = time.time() - start_time

while True
  print(getSpeeds())
  time.sleep(0.3)
  if elapsed_time == 10
    break
