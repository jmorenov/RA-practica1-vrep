#!/usr/bin/python

import connection
import reactivecontrollerv110 as robotController

remoteConnection = connection.RemoteConnection()
remoteConnection.run(robotController.controller)