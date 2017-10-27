import time
import numpy as np

PROXIMITY_LIMIT = 0.3

def controller(remoteConnection):
    counter = 0

    while (remoteConnection.getConnectionId() != -1 and counter < 1):

        #remoteConnection.setLeftMotorVelocity(-50)
        #remoteConnection.setRightMotorVelocity(50)
        remoteConnection.setAngle(90, 0.2)
        time.sleep(0.2)

        remoteConnection.printMessage('2')
        remoteConnection.setLeftMotorVelocity(0)
        remoteConnection.setRightMotorVelocity(0)
        time.sleep(0.005)
        remoteConnection.printMessage('3')

        counter += 1
