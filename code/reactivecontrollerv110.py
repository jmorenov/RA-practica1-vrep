import time
import numpy as np
import random

PROXIMITY_LIMIT_ALL = 0.1
PROXIMITY_LIMIT_FRONT = 0.7
VELOCITY_BASE = 1.0
VELOCITY_MAX = 2.0
VELOCITY_MIN = 0.5
TIME_STEP = 0.010

def controller(remoteConnection):
    lspeed = +VELOCITY_BASE
    rspeed = +VELOCITY_BASE
    endSimulation = False

    while (remoteConnection.isConnectionEstablished() and endSimulation == False):
        proximitySonars = np.array(remoteConnection.readAllSensors(8))

        if proximitySonars.min() <= PROXIMITY_LIMIT_ALL:
            minProximityIndex = proximitySonars.argmin()

            if minProximityIndex == 3 or minProximityIndex == 4:
                remoteConnection.printMessage('Collision detected! Simulation ended')
                lspeed = 0.0
                rspeed = 0.0
            else:
                minProximityOrientation = remoteConnection.getSensorAngle(minProximityIndex + 1)
                randomOrientation = random.uniform(-10, +10)
                remoteConnection.setAngle(minProximityOrientation + randomOrientation)
        elif proximitySonars[3] <= PROXIMITY_LIMIT_FRONT or proximitySonars[4] <= PROXIMITY_LIMIT_FRONT:
            maxDistanceIndex = proximitySonars.argmax()

            if (proximitySonars[maxDistanceIndex] == 1):
                maxDistanceIndexes = np.where(proximitySonars == 1)[0]
                maxDistanceIndex = random.randint(0, len(maxDistanceIndexes) - 1)

            maxDistanceOrientation = remoteConnection.getSensorAngle(maxDistanceIndex + 1)
            randomOrientation = random.uniform(0, maxDistanceOrientation)
            remoteConnection.setAngle(randomOrientation)
        else:
            if lspeed < VELOCITY_MAX and rspeed < VELOCITY_MAX and proximitySonars.min() == 1:
                lspeed += 0.1
                rspeed += 0.1
            elif lspeed > VELOCITY_MIN and rspeed > VELOCITY_MIN and proximitySonars.min() != 1:
                lspeed -= 0.1
                rspeed -= 0.1

        remoteConnection.setLeftMotorVelocity(lspeed)
        remoteConnection.setRightMotorVelocity(rspeed)

        time.sleep(TIME_STEP)