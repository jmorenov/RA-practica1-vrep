#!/usr/bin/python

import sys
import vrep
import time
import datetime

def read_sonar(clientID, sonar):
    retcode, activated, point, dummy1, dummy2 = vrep.simxReadProximitySensor(clientID, sonar, vrep.simx_opmode_streaming)
    if retcode != vrep.simx_return_ok:
        printMessage(clientID, 'Failed reading proximity sensor id= ' + str(sonar) + str(retcode))
    else:
        if activated:
            return point[2]
        else:
            return 1.0

def printMessage(clientID, message):
    message = '### ' + str(datetime.datetime.now().time()) + ' | ' + message
    returnCode = vrep.simxAddStatusbarMessage(clientID, message, vrep.simx_opmode_oneshot)

    return returnCode

vrep.simxFinish(-1) # just in case, close all opened connections

port = int(sys.argv[1])
lmh  = int(sys.argv[2])
rmh  = int(sys.argv[3])
sonar2 = int(sys.argv[4])
sonar4 = int(sys.argv[5])
sonar5 = int(sys.argv[6])
sonar7 = int(sys.argv[7])

# Connect to V-REP
clientID = vrep.simxStart('127.0.0.1', port, True, True, 2000, 5)
printMessage(clientID, 'Number of arguments: ' + str(len(sys.argv)) + 'arguments.')
printMessage(clientID, 'Argument List: ' + str(sys.argv))
printMessage(clientID, 'Program started')

if clientID == -1:
    printMessage(clientID, 'Failed connecting to remote API server')
else:
    printMessage(clientID, 'sonar2 =' + str(read_sonar(clientID, sonar2)))
    printMessage(clientID, 'sonar4 =' + str(read_sonar(clientID, sonar4)))
    printMessage(clientID, 'sonar5 =' + str(read_sonar(clientID, sonar5)))
    printMessage(clientID, 'sonar7 =' + str(read_sonar(clientID, sonar7)))

    print ('Connected to remote API server')
    while (vrep.simxGetConnectionId(clientID) != -1):
        if read_sonar(clientID, sonar4) < 0.8 or read_sonar(clientID, sonar5) < 0.3:
            lspeed = -1.0
            rspeed = +1.7
        elif read_sonar(clientID, sonar2) < 0.7:
            lspeed = +1.2
            rspeed = +1.5            
        elif read_sonar(clientID, sonar7) < 0.3:
            lspeed = +0.1
            rspeed = +1.4            
        else:
            lspeed = +1.2
            rspeed = +0.5

        vrep.simxSetJointTargetVelocity(clientID, lmh, lspeed, vrep.simx_opmode_oneshot)
        vrep.simxSetJointTargetVelocity(clientID, rmh, rspeed, vrep.simx_opmode_oneshot)
        time.sleep(0.005)

    printMessage(clientID, 'sonar2 =' + str(read_sonar(clientID, sonar2)))
    printMessage(clientID, 'sonar4 =' + str(read_sonar(clientID, sonar4)))
    printMessage(clientID, 'sonar5 =' + str(read_sonar(clientID, sonar5)))
    printMessage(clientID, 'sonar7 =' + str(read_sonar(clientID, sonar7)))

    # Close the connection to V-REP
    vrep.simxFinish(clientID)

printMessage(clientID, 'Program ended')
