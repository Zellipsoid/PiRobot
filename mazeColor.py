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

def mainMenu(options):
    selection = input('(P) Change Robot Position. Enter as <P x y heading>.\n(M) Create new map. Enter as <M>.\n(C) Choose to find pink, yellow, green, or blue. Enter as <C color>.\n(E) Exit. Enter as <E>\nEnter selection: ')
    selection = selection.split(' ')
    if selection[0].lower() == 'p':
        try:
            pos = [int(selection[1]), int(selection[2])]
        except ValueError:
            print('Error: x and y must be integers')
            return options
        if pos[0] > 3 or pos[0] < 0 or pos[1] > 3 or pos[1] < 0:
            print('Error: positions must be 0, 1, 2, or 3')
            return options
        heading = selection[3].lower()
        if heading != 'n' and heading != 's' and heading != 'e' and heading != 'w':
            print('Error: heading must be N, E, S, or W')
            return options
        options['pos'] = pos
        options['heading'] = heading
        print('Position set!')
    elif selection[0].lower() == 'm':
        if (options['heading'] == 'unknown' or options['pos'] == (-1, -1)):
            print('Error: must set position first')
        else:
            options['readyToMap'] = True
            print('Mapping...')
    elif selection[0].lower() == 'c':
        if options['mapped']:
            if selection[1].lower() == 'pink':
                options['color'] = 'pink'
                print('Color set!')     
            elif selection[1].lower() == 'yellow':
                options['color'] = 'yellow'
                print('Color set!')
            elif selection[1].lower() == 'green':
                options['color'] = 'green'
                print('Color set!')
            elif selection[1].lower() == 'blue':
                options['color'] = 'blue'
                print('Color set, plotting...')
            else:
                print('Error: color must be pink, yellow, green, or blue')
        else:
            print('Error: must construct map first')
    elif selection[0].lower() == 'e':
        exit()
    else:
        print('Error: must select P, M, C, or E')
    return options



# if len(sys.argv) != 4:
#     sys.exit('Error: navigateMaze.py requires 3 arguments: x position, y position, and heading')
# try:
#     pos = [int(sys.argv[1]), int(sys.argv[2])]
# except ValueError:
#     sys.exit('Error: arguments must be integers: x position, y position')
# heading = str(sys.argv[3].lower())
# if heading != 'n' and heading != 's' and heading != 'e' and heading != 'w':
#     sys.exit('Error: heading must be N, E, S, or W')
# if pos[0] > 3 or pos[0] < 0 or pos[1] > 3 or pos[1] < 0:
#     sys.exit('Error: positions must be 0, 1, 2, or 3')

#Todo:
#Make robot stop going forward and return to cell if detects wall in front of it and less than ~2 inches moved
#Make robot navigate randomly; will need to pass in data telling maze not to print map

options = {'color': 'unknown', 'readyToMap': False, 'pos': (-1, -1), 'heading': 'unknown'}

while options['pos'] == (-1, -1) or options['heading'] == 'unknown': #make sure has position
    options = mainMenu(options)

mz = maze.Maze(options['pos'], options['heading'])

while True: #now can choose any option
    if options['readyToMap'] == True:
        if mz.nav.mapComplete == True: #clear map
            mz.nav.clearMap(options['pos'], options['heading'])
        mz.analyzeCell(True)
        while mz.goToNextCell():
            pass
        print('DONE!')
        options['readyToMap'] = False
        options['mapped'] = True

    if options['color'] != 'unknown':
        print('not ready yet :(')
        options['color'] = 'unknown'
    options = mainMenu(options)
    print(options)