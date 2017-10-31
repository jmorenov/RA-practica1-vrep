import time
import numpy as np
import random

PROXIMITY_LIMIT = 0.3

def controller(remoteConnection):
    lspeed = +1.0
    rspeed = +1.0

    while remoteConnection.getConnectionId() != -1:
        remoteConnection.setLeftMotorVelocity(lspeed)
        remoteConnection.setRightMotorVelocity(rspeed)

        position = remoteConnection.getPosition()

        remoteConnection.printMessage(str(position))

        time.sleep(0.010)
