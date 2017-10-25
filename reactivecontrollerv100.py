import time
import numpy as np

PROXIMITY_LIMIT = 0.3

def controller(remoteConnection):
    oldMsg = msg = ''
    inRotation = False
    lspeed = +1.0
    rspeed = +1.0

    while (remoteConnection.getConnectionId() != -1):
        dataSonars = np.array(remoteConnection.readAllSensors(8))
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

        # msg = 'left: ' + str(lspeed) + '|x right: ' + str(rspeed)

        remoteConnection.setLeftMotorVelocity(lspeed)
        remoteConnection.setRightMotorVelocity(rspeed)

        '''if oldMsg != msg:
            printMessage(clientID, msg)
            oldMsg = msg'''

        time.sleep(0.005)