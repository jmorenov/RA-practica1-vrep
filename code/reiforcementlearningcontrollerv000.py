import time
import numpy as np
import random

def controller(remoteConnection):
    PROXIMITY_LIMIT = 0.1
    TIME_STEP = 0.010
    VELOCITY_BASE = 1.0
    EPSILON = 0.3
    S = list() # [x, y, range]
    A = list()
    Q = list()
    lspeed = +VELOCITY_BASE
    rspeed = +VELOCITY_BASE
    state = -1
    actionIndex = 0

    def getState(position):
        for i in range(0, len(S)):
            if position[0] <= S[i][0] + S[i][2] and position[0] >= S[i][0] - S[i][2]:
                if position[1] <= S[i][1] + S[i][2] and position[1] >= S[i][1] - S[i][2]:
                    return i
        return -1

    def addNewState(robotPosition, range):
        S.append([robotPosition[0], robotPosition[1], range])

        return len(S) - 1

    def addActionsToQ(proximitySensors):
        Q.append(proximitySensors)

    def getReward(proximitySensors):
        proximitySensors = np.array(proximitySensors)

        return proximitySensors.sum()

    def getAnglesOfSensors():
        angles = []

        for i in range(1, 17):
            angles = np.append(angles, remoteConnection.getSensorAngle(i))

        return angles

    def addActionsToState(angles):
        A.append(angles)

    def createNewState():
        sensors = np.array(remoteConnection.readAllSensors())
        range = sensors.min()
        newState = addNewState(position, range)
        addActionsToQ(sensors)
        angles = getAnglesOfSensors()
        addActionsToState(angles)

        return newState

    while remoteConnection.isConnectionEstablished():
        position = remoteConnection.getPosition()
        actualState = getState(position)
        sensors = np.array(remoteConnection.readAllSensors())

        if state != actualState or state == -1:
            if actualState == -1: # New state
                newState = createNewState()
                actualState = newState

            if state == -1:
                state = actualState

            reward = getReward(sensors)

            # r' = reward y s' = actualState
            # Actualizar el valor de Q(s, a)
            Q[state][actionIndex] += reward + np.max(Q[actualState])
            Q[state][actionIndex] = max(Q[state][actionIndex], 1)

            if random.uniform(0, 1) <= EPSILON: # Elegir aleatoriamente a
                EPSILON -= 0.005

                while True:
                    actionIndex = random.randint(0, 16)
                    action = A[actualState][actionIndex]
                    proximity = Q[actualState][actionIndex]

                    if proximity > PROXIMITY_LIMIT:
                        break
            else: # Elegir a con mayor probabilidad
                actionIndex = np.argmax(Q[actualState])
                action = A[actualState][actionIndex]

            remoteConnection.setAngle(action)
            remoteConnection.setLeftMotorVelocity(lspeed)
            remoteConnection.setRightMotorVelocity(rspeed)
            state = actualState


        time.sleep(TIME_STEP)
