import time
import numpy as np

PROXIMITY_LIMIT = 0.3
VELOCITY_BASE = 1.0
VELOCITY_TURN = 2.0
TIME_STEP = 0.005

def controller(remoteConnection):
    inRotation = False
    lspeed = +VELOCITY_BASE
    rspeed = +VELOCITY_BASE

    while (remoteConnection.isConnectionEstablished()):
        dataSonars = np.array(remoteConnection.readAllSensors(8))
        minProximity = dataSonars.min()

        if (minProximity <= PROXIMITY_LIMIT and inRotation == False):
            inRotation = True
            i = dataSonars.argmin()
            if (i <= 4):
                lspeed = +VELOCITY_TURN
                rspeed = -VELOCITY_TURN
            else:
                lspeed = -VELOCITY_TURN
                rspeed = +VELOCITY_TURN
        elif inRotation == False or minProximity > PROXIMITY_LIMIT:
            lspeed = +VELOCITY_BASE
            rspeed = +VELOCITY_BASE
            inRotation = False

        remoteConnection.setLeftMotorVelocity(lspeed)
        remoteConnection.setRightMotorVelocity(rspeed)

        time.sleep(TIME_STEP)