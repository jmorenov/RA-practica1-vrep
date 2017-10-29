#!/usr/bin/python

import connection
import reactivecontrollerv120 as robotController

remoteConnection = connection.RemoteConnection()
remoteConnection.run(robotController.controller)