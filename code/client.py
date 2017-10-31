#!/usr/bin/python

import connection
import reiforcementlearningcontrollerv000 as robotController

remoteConnection = connection.RemoteConnection()
remoteConnection.run(robotController.controller)