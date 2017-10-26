import time
import numpy as np

PROXIMITY_LIMIT = 0.3

def controller(remoteConnection):
    remoteConnection.setAngle(90, 0.005)
    time.sleep(0.010)

    while (remoteConnection.getConnectionId() != -1):
        remoteConnection.setLeftMotorVelocity(0)
        remoteConnection.setRightMotorVelocity(0)

        time.sleep(0.005)