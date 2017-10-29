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

        if proximitySonars.min() <= 0.2:
            minProximityIndex = proximitySonars.argmin()

            if minProximityIndex == 3 or minProximityIndex == 4:
                remoteConnection.printMessage('Collision detected! Simulation ended')
                lspeed = 0.0
                rspeed = 0.0
                endSimulation = True
            else:
                if minProximityIndex <= 3:
                    interval = -5
                else:
                    interval = +5

                randomOrientation = random.uniform(0, interval)
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