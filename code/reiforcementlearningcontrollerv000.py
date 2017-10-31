import time
import numpy as np

PROXIMITY_LIMIT = 0.2
TIME_STEP = 0.010
VELOCITY_BASE = 1.0
EPSILON = 0.7

def controller(remoteConnection):
    S = [] # [x, y, range]
    A = []
    Q = []
    lspeed = +VELOCITY_BASE
    rspeed = +VELOCITY_BASE
    state = 0

    def getState(position):
        for i in range(0, len(S)):
            if position[0] <= S[i][0] + S[i][3] and position[0] >= S[i][0] - S[i][3]:
                if position[1] <= S[i][1] + S[i][3] and position[1] >= S[i][1] - S[i][3]:
                    return i
            return -1

    def addNewState(robotPosition, range):
        np.append(S, [robotPosition[0], robotPosition[1], range])

        return len(S) - 1

    def addActionsToQ(state, proximitySensors):
        Q[state] = proximitySensors

    def getReward(proximitySensors):
        proximitySensors = np.array(proximitySensors)

        return proximitySensors.sum()

    while remoteConnection.isConnectionEstablished():
        position = remoteConnection.getPosition()
        actualState = getState(position)

        if state != actualState:
            sensors = np.array(remoteConnection.readAllSensors())
            reward = getReward(sensors)

            if actualState == -1:
                range = sensors.min()
                newState = addNewState(position, range)
                addActionsToQ(newState, sensors)
                # addActionsToState(newState, angles of the sensors)
                state = newState

            # Elegir a desde s usando la política derivada de Q.
            # Realizar la acción a, observar r' y s'
            # Actualizar el valor de Q(s, a)

            remoteConnection.setLeftMotorVelocity(lspeed)
            remoteConnection.setRightMotorVelocity(rspeed)

        time.sleep(TIME_STEP)
