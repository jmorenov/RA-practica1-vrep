import time
import numpy as np
import random

PROXIMITY_LIMIT = 0.3

def controller(remoteConnection):
    lspeed = +1.0
    rspeed = +1.0
    endSimulation = False

    while (remoteConnection.getConnectionId() != -1 and endSimulation == False):
        proximitySonars = np.array(remoteConnection.readAllSensors(8))

        if proximitySonars.min() <= 0.1:
            minProximityIndex = proximitySonars.argmin()

            if minProximityIndex == 3 or minProximityIndex == 4:
                remoteConnection.printMessage('Collision detected! Simulation ended')
                lspeed = 0.0
                rspeed = 0.0
            else:
                minProximityOrientation = remoteConnection.getSensorAngle(minProximityIndex + 1)
                randomOrientation = random.uniform(-10, +10)
                remoteConnection.setAngle(minProximityOrientation + randomOrientation)
        elif proximitySonars[3] <= 0.7 or proximitySonars[4] <= 0.7:
            maxDistanceIndex = proximitySonars.argmax()

            if (proximitySonars[maxDistanceIndex] == 1):
                maxDistanceIndexes = np.where(proximitySonars == 1)[0]
                maxDistanceIndex = random.randint(0, len(maxDistanceIndexes) - 1)

            maxDistanceOrientation = remoteConnection.getSensorAngle(maxDistanceIndex + 1)
            randomOrientation = random.uniform(0, maxDistanceOrientation)
            remoteConnection.setAngle(randomOrientation)
        else:
            if lspeed < 2.0 and rspeed < 2.0 and proximitySonars.min() == 1:
                lspeed += 0.1
                rspeed += 0.1
            elif lspeed > 0.5 and rspeed > 0.5 and proximitySonars.min() != 1:
                lspeed -= 0.1
                rspeed -= 0.1

        remoteConnection.setLeftMotorVelocity(lspeed)
        remoteConnection.setRightMotorVelocity(rspeed)

        time.sleep(0.010)