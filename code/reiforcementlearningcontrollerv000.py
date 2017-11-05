import time
import numpy as np
import random
import math

def controller(remoteConnection):
    PROXIMITY_LIMIT = 0.4
    TIME_STEP = 0.005
    VELOCITY_BASE = 0.5
    EPSILON = 0.3
    S = list() # [x, y, range]
    A = list()
    Q = list()
    lspeed = +VELOCITY_BASE
    rspeed = +VELOCITY_BASE
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
        for i in range(8, 16):
            proximitySensors[i] = normalizeValue(proximitySensors[i] - 0.5)

        Q.append(proximitySensors)

    def calculateDistance(position1, position2):
        return math.sqrt((position2[0] - position1[0]) ** 2 + (position2[1] - position1[1]) ** 2)

    def setReward(oldPosition, proximitySensors, oldReward):
        if proximitySensors.min() <= PROXIMITY_LIMIT:
            reward = 0
        else:
            actualPosition = remoteConnection.getPosition()
            distance = calculateDistance(oldPosition, actualPosition)
            distanceReward =  distance * 0.4
            proximityReward = proximitySensors.sum() * 0.6
            reward = oldReward + distanceReward + proximityReward

        return reward

    def getAnglesOfSensors():
        angles = []

        for i in range(1, 17):
            angles = np.append(angles, remoteConnection.getSensorAngle(i))

        return angles

    def addActionsToState(angles):
        A.append(angles)

    def createNewState(sensors, position):
        range = sensors.min()
        newState = addNewState(position, range)
        addActionsToQ(sensors)
        angles = getAnglesOfSensors()
        addActionsToState(angles)

        return newState

    def normalizeValue(value):
        if value > 1:
            return 1
        elif value < 0:
            return 0
        else:
            return value

    lastPosition = remoteConnection.getPosition()
    state = getState(lastPosition)
    action = None

    while remoteConnection.isConnectionEstablished():
        position = remoteConnection.getPosition()
        actualState = getState(position)
        proximitySensors = np.array(remoteConnection.readAllSensors())
        proximityFrontalSensors = np.array(proximitySensors[2:5])

        possibleCollision = proximityFrontalSensors.min() <= PROXIMITY_LIMIT

        if state != actualState or possibleCollision == True:

            if actualState == -1: # New state
                newState = createNewState(proximitySensors, position)
                actualState = newState

            # r' = reward y s' = actualState
            # Actualizar el valor de Q(s, a)
            Q[state][actionIndex] = setReward(lastPosition, proximityFrontalSensors, Q[state][actionIndex])

            if possibleCollision == True or action != None: # Mayor probabilidad de mantener la misma direccion
                if random.uniform(0, 1) <= EPSILON: # Elegir aleatoriamente a
                    EPSILON -= 0.002

                    while True:
                        actionIndex = random.randint(0, 15)
                        action = A[actualState][actionIndex]
                        proximity = Q[actualState][actionIndex]

                        if proximity > PROXIMITY_LIMIT:
                            break
                else: # Elegir a con mayor probabilidad
                    actionIndex = np.argmax(Q[actualState])
                    action = A[actualState][actionIndex]

            lastPosition = remoteConnection.getPosition()
            state = actualState

            remoteConnection.setAngle(action)
            remoteConnection.setLeftMotorVelocity(lspeed)
            remoteConnection.setRightMotorVelocity(rspeed)

        time.sleep(TIME_STEP)
