import time
import numpy as np
import vrep

PROXIMITY_LIMIT = 0.3

def controller(remoteConnection):
    lspeed = +1.0
    rspeed = +1.0
    endSimulation = False

    while (remoteConnection.getConnectionId() != -1 and endSimulation == False):
        proximitySonars = np.array(remoteConnection.readAllSensors(8))

        if proximitySonars[3] <= 0.3 or proximitySonars[4] <= 0.3:
            remoteConnection.printMessage('Collision detected! Simulation ended')
            #remoteConnection.printMessage(str(orientationSonars))
            #remoteConnection.setAngle(90)
            lspeed = 0.0
            rspeed = 0.0
            endSimulation = True
        '''else:
            maxDistanceIndex = proximitySonars.argmax()
            maxDistanceOrientation = orientationSonars[maxDistanceIndex]
            remoteConnection.setAngle(maxDistanceOrientation)'''

        remoteConnection.printMessage(str(remoteConnection.getSensorAngle(8)))
        #remoteConnection.printMessage(str(remoteConnection.getSensorAngle(4)))

        remoteConnection.setLeftMotorVelocity(lspeed)
        remoteConnection.setRightMotorVelocity(rspeed)