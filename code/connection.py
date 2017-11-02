import sys
import vrep
import datetime
import math

class RemoteConnection:

    def __init__(self):
        self.numberOfArguments = str(len(sys.argv))
        self.argumentList = str(len(sys.argv))
        self.port = int(sys.argv[1])
        self.robotHandle = int(sys.argv[2])
        self.leftMotorHandle = int(sys.argv[3])
        self.rightMotorHandle = int(sys.argv[4])
        self.sensorName = str(sys.argv[5])

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
            except NameError as error:
                self.printMessage(str(error.message))
            except ValueError as error:
                self.printMessage(str(error.message))
            except ZeroDivisionError as error:
                self.printMessage(str(error.message))
            except IndexError as error:
                self.printMessage(str(error.message))
            except TypeError as error:
                self.printMessage(str(error.message))
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

    def readAllSensors(self, numberOfSensorsToRead = 16, proximityValueForUnactivatedSensors = 1.0):
        s = vrep.simxGetObjectGroupData(self.clientID, vrep.sim_object_proximitysensor_type, 13, vrep.simx_opmode_blocking)
        proximity = []

        for i in range(numberOfSensorsToRead):
            if s[2][2 * i] == 1:
                proximity.append(s[3][6 * i + 2])
            else:
                proximity.append(proximityValueForUnactivatedSensors)

        return proximity

    def getConnectionId(self):
        return vrep.simxGetConnectionId(self.clientID)

    def setLeftMotorVelocity(self, velocity):
        vrep.simxSetJointTargetVelocity(self.clientID, self.leftMotorHandle, velocity, vrep.simx_opmode_oneshot)
        vrep.simxSynchronousTrigger(self.clientID)

    def setRightMotorVelocity(self, velocity):
        vrep.simxSetJointTargetVelocity(self.clientID, self.rightMotorHandle, velocity, vrep.simx_opmode_oneshot)
        vrep.simxSynchronousTrigger(self.clientID)

    def getAngle(self):
        ret, eulerAngles = vrep.simxGetObjectOrientation(self.clientID, self.robotHandle, -1, vrep.simx_opmode_oneshot)

        return math.degrees(eulerAngles[2])

    def getPosition(self):
        ret, position = vrep.simxGetObjectPosition(self.clientID, self.robotHandle, -1, vrep.simx_opmode_oneshot)

        return position

    def getSensorAngle(self, sensorNumber):
        err, sensorHandle = vrep.simxGetObjectHandle(self.clientID, self.sensorName + str(sensorNumber),
                                                vrep.simx_opmode_blocking)
        ret, eulerAngles = vrep.simxGetObjectOrientation(self.clientID, sensorHandle, -1,
                                                         vrep.simx_opmode_oneshot)

        angle = math.fabs(math.degrees(eulerAngles[1]))

        if (sensorNumber - 1 >= 5 and sensorNumber - 1 <= 12):
            return angle + 90
        else:
            return angle - 90


    def setAngle(self, angleToRotate):
        if angleToRotate == 0.0:
            return

        speedRotation = 0.5
        sign = angleToRotate / math.fabs(angleToRotate)

        self.setLeftMotorVelocity(speedRotation * sign)
        self.setRightMotorVelocity(-speedRotation * sign)
        vrep.simxSynchronousTrigger(self.clientID)

        previousAngle = self.getAngle()
        rotation = 0

        while math.fabs(rotation) <= math.fabs(angleToRotate):
            angle = self.getAngle()
            da = angle - previousAngle

            if da > 0:
                da = math.fmod(da + math.pi, 2 * math.pi) - math.pi
            else:
                da = math.fmod(da - math.pi, 2 * math.pi) + math.pi

            rotation += da
            previousAngle = angle
            #self.printMessage(str(rotation) + ' ' + str(angleToRotate))

        self.setLeftMotorVelocity(0)
        self.setRightMotorVelocity(0)
        vrep.simxSynchronousTrigger(self.clientID)

    def isConnectionEstablished(self):
        return self.getConnectionId() != -1