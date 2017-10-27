import sys
import vrep
import datetime
import math
import time

class RemoteConnection:

    def __init__(self):
        self.numberOfArguments = str(len(sys.argv))
        self.argumentList = str(len(sys.argv))
        self.port = int(sys.argv[1])
        self.leftMotorHandle = int(sys.argv[2])
        self.rightMotorHandle = int(sys.argv[3])

    def run(self, controller):
        vrep.simxFinish(-1)  # just in case, close all opened connections

        # Connect to V-REP
        self.clientID = vrep.simxStart('127.0.0.1', self.port, True, True, 2000, 5)
        self.printMessage('Program started')

        if self.clientID == -1:
            self.printMessage('Failed connecting to remote API server')
        else:
            self.printMessage('Connected to remote API server')

            try:
                controller(self)
            except AttributeError as error:
                self.printMessage(str(error.message))
            except:
                self.printMessage(str(sys.exc_info()[0]))

            # Close the connection to V-REP
            vrep.simxFinish(self.clientID)

    def printMessage(self, message):
        message = '### ' + str(datetime.datetime.now().time()) + ' | ' + message
        returnCode = vrep.simxAddStatusbarMessage(self.clientID, message, vrep.simx_opmode_oneshot_wait)

        return returnCode

    def readASensor(self, sensor):
        retcode, activated, point, dummy1, dummy2 = vrep.simxReadProximitySensor(self.clientID, sensor, vrep.simx_opmode_streaming)
        if retcode != vrep.simx_return_ok:
            self.printMessage('Failed reading proximity sensor id= ' + str(sensor) + str(retcode))
        else:
            if activated:
                return point[2]
            else:
                return 1.0

    def readAllSensors(self, numberOfSensorsToRead = 16):
        s = vrep.simxGetObjectGroupData(self.clientID, vrep.sim_object_proximitysensor_type, 13, vrep.simx_opmode_blocking)
        r = []
        for i in range(numberOfSensorsToRead):
            if s[2][2 * i] == 1:
                r.append(s[3][6 * i + 2])
            else:
                r.append(1.0)
        return r

    def getConnectionId(self):
        return vrep.simxGetConnectionId(self.clientID)

    def setLeftMotorVelocity(self, velocity):
        vrep.simxSetJointTargetVelocity(self.clientID, self.leftMotorHandle, velocity, vrep.simx_opmode_oneshot)

    def setRightMotorVelocity(self, velocity):
        vrep.simxSetJointTargetVelocity(self.clientID, self.rightMotorHandle, velocity, vrep.simx_opmode_oneshot)

    def setAngle(self, angle, timeValue):
        angle = math.radians(angle)
        angularVelocity = angle/(timeValue)

        if (angle > 0):
            self.setLeftMotorVelocity(angularVelocity/2)
            self.setRightMotorVelocity(-angularVelocity/2)
        else:
            self.setRightMotorVelocity(angularVelocity)

        #time.sleep(1.0)