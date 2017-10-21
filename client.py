#!/usr/bin/python

import sys
import vrep
import time
import datetime

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
#sonar2 = int(sys.argv[4])
#sonar4 = int(sys.argv[5])
#sonar5 = int(sys.argv[6])
#sonar7 = int(sys.argv[7])

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
    while (vrep.simxGetConnectionId(clientID) != -1):
        dataSonars = read_all_sonar(clientID, 8)

        lspeed = 1.0
        rspeed = 1.0

        for i in range(len(dataSonars)):
            if (dataSonars[i] <= PROXIMITY_LIMIT):
                if (i <= 4):
                    rspeed = -1.0
                    lspeed = +2.0
                else:
                    lspeed = -1.0
                    rspeed = +2.0
                break

        msg = 'left: ' + str(lspeed) + '| right: ' + str(rspeed)

        '''
        if dataSonars[3] < 0.8 or dataSonars[4] < 0.3:
            lspeed = -1.0
            rspeed = +1.7
            msg = 'turn left'
        elif dataSonars[1] < 0.7:
            lspeed = +1.2
            rspeed = +1.5
            msg = 'recto left'
        elif dataSonars[6] < 0.3:
            lspeed = +0.1
            rspeed = +1.4
            msg = 'turn left'
        else:
            lspeed = +1.0
            rspeed = +1.0
            msg = 'recto'
        '''

        vrep.simxSetJointTargetVelocity(clientID, lmh, lspeed, vrep.simx_opmode_oneshot)
        vrep.simxSetJointTargetVelocity(clientID, rmh, rspeed, vrep.simx_opmode_oneshot)


        '''if oldMsg != msg:
            printMessage(clientID, msg)
            oldMsg = msg'''


        time.sleep(0.005)

    # Close the connection to V-REP
    vrep.simxFinish(clientID)

printMessage(clientID, 'Program ended')
