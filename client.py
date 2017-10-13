#!/usr/bin/python

import sys
import vrep
import time


def read_sonar(clientID, sonar):
    retcode, activated, point, dummy1, dummy2 = vrep.simxReadProximitySensor(clientID, sonar, vrep.simx_opmode_streaming)
    if retcode != vrep.simx_return_ok:
        print('### Failed reading proximity sensor id=', sonar, retcode)
    else:
        if activated:
            return point[2]
        else:
            return 1.0


print('### Program started')
vrep.simxFinish(-1) # just in case, close all opened connections

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)

port = int(sys.argv[1])
lmh  = int(sys.argv[2])
rmh  = int(sys.argv[3])
sonar2 = int(sys.argv[4])
sonar4 = int(sys.argv[5])
sonar5 = int(sys.argv[6])
sonar7 = int(sys.argv[7])

# Connect to V-REP
clientID = vrep.simxStart('127.0.0.1', port, True, True, 2000, 5)
if clientID == -1:
    print ('### Failed connecting to remote API server')
else:
    # print 'sonar2 =', read_sonar(clientID, sonar2)
    # print 'sonar4 =', read_sonar(clientID, sonar4)
    # print 'sonar5 =', read_sonar(clientID, sonar5)
    # print 'sonar7 =', read_sonar(clientID, sonar7)

    print ('### Connected to remote API server')
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

    # print 'sonar2 =', read_sonar(clientID, sonar2)
    # print 'sonar4 =', read_sonar(clientID, sonar4)
    # print 'sonar5 =', read_sonar(clientID, sonar5)
    # print 'sonar7 =', read_sonar(clientID, sonar7)

    # Close the connection to V-REP
    vrep.simxFinish(clientID)

print ('### Program ended')
