#!/usr/bin/python

import sys
import vrep
import time
import datetime
import numpy as np

PROXIMITY_LIMIT = 0.3

def read_sonar(clientID, sonar):
    retcode, activated, point, dummy1, dummy2 = vrep.simxReadProximitySensor(clientID, sonar, vrep.simx_opmode_streaming)
    if retcode != vrep.simx_return_ok:
        printMessage(clientID, 'Failed reading proximity sensor id= ' + str(sonar) + str(retcode))
    else:
        if activated:
            return point[2]
        else:
            return 1.0

def read_all_sonar(clientID, maxSensonrs = 16):
    s = vrep.simxGetObjectGroupData(clientID,
                vrep.sim_object_proximitysensor_type, 13,
                vrep.simx_opmode_blocking)
    r = []
    for i in range(maxSensonrs):
        if s[2][2*i] == 1:
            r.append(s[3][6*i+2])
        else:
            r.append(1.0)
    return r

def printMessage(clientID, message):
    message = '### ' + str(datetime.datetime.now().time()) + ' | ' + message
    returnCode = vrep.simxAddStatusbarMessage(clientID, message, vrep.simx_opmode_oneshot)

    return returnCode

vrep.simxFinish(-1) # just in case, close all opened connections

port = int(sys.argv[1])
lmh  = int(sys.argv[2])
rmh  = int(sys.argv[3])

# Connect to V-REP
clientID = vrep.simxStart('127.0.0.1', port, True, True, 2000, 5)
printMessage(clientID, 'Number of arguments: ' + str(len(sys.argv)) + 'arguments.')
printMessage(clientID, 'Argument List: ' + str(sys.argv))
printMessage(clientID, 'Program started')

if clientID == -1:
    printMessage(clientID, 'Failed connecting to remote API server')
else:
    print ('Connected to remote API server')
    oldMsg = msg = ''
    inRotation = False
    lspeed = +1.0
    rspeed = +1.0

    while (vrep.simxGetConnectionId(clientID) != -1):
        dataSonars = np.array(read_all_sonar(clientID, 8))
        minProximity = dataSonars.min()

        if (minProximity <= 0.3 and inRotation == False):
            inRotation = True
            i = dataSonars.argmax()
            if (i <= 4):
                lspeed = +2.0
                rspeed = -2.0
            else:
                lspeed = -2.0
                rspeed = +2.0
        elif inRotation == False or minProximity > 0.3:
            lspeed = +1.0
            rspeed = +1.0
            inRotation = False

        #msg = 'left: ' + str(lspeed) + '|x right: ' + str(rspeed)

        vrep.simxSetJointTargetVelocity(clientID, lmh, lspeed, vrep.simx_opmode_oneshot)
        vrep.simxSetJointTargetVelocity(clientID, rmh, rspeed, vrep.simx_opmode_oneshot)

        '''if oldMsg != msg:
            printMessage(clientID, msg)
            oldMsg = msg'''

        time.sleep(0.005)

    # Close the connection to V-REP
    vrep.simxFinish(clientID)

printMessage(clientID, 'Program ended')
