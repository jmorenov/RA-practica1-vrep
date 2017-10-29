-- Default timing for automatic thread switching
simSetThreadSwitchTiming(2)

-- Get some handles first:
local leftMotor  = simGetObjectHandle("Pioneer_p3dx_leftMotor")
local rightMotor = simGetObjectHandle("Pioneer_p3dx_rightMotor")
local robot = simGetObjectHandle("Pioneer_p3dx")

-- Set the sensors string:
local sensors = "Pioneer_p3dx_ultrasonicSensor"

-- Choose a port that is probably not used (try to always use a similar code):
simSetThreadAutomaticSwitch(false)
local portNb    = simGetInt32Parameter(sim_intparam_server_port_next)
local portStart = simGetInt32Parameter(sim_intparam_server_port_start)
local portRange = simGetInt32Parameter(sim_intparam_server_port_range)
local newPortNb = portNb + 1
if (newPortNb >= portStart + portRange) then
    newPortNb = portStart
end
simSetInt32Parameter(sim_intparam_server_port_next, newPortNb)
simSetThreadAutomaticSwitch(true)

-- Check what OS we are using:
platf = simGetInt32Parameter(sim_intparam_platform)
if (platf == 0) then
    pluginFile = 'v_repExtRemoteApi.dll'
end
if (platf == 1) then
    pluginFile = 'libv_repExtRemoteApi.dylib'
end
if (platf == 2) then
    pluginFile = 'libv_repExtRemoteApi.so'
end

-- Check if the required remote Api plugin is there:
moduleName = 0
moduleVersion = 0
index = 0
pluginNotFound = true
while moduleName do
    moduleName,moduleVersion = simGetModuleName(index)
    if (moduleName == 'RemoteApi') then
        pluginNotFound = false
    end
    index = index + 1
end

if (pluginNotFound) then
    -- Plugin was not found
    simDisplayDialog('Error',"Remote Api plugin was not found. ('"..pluginFile.."')&&nSimulation will not run properly",sim_dlgstyle_ok,true,nil,{0.8,0,0,0,0,0},{0.5,0,0,1,1,1})
else
    -- Ok, we found the plugin.
    -- We first start the remote Api server service (this requires the v_repExtRemoteApi plugin):
    simExtRemoteApiStart(portNb) -- this server function will automatically close again at simulation end

    -- Now we start the client application:
    -- result = simLaunchExecutable("programming/pioneer/bin/client", portNb.." "..leftMotor.." "..rightMotor.." "..sonar4.." "..sonar5, 0) -- set the last argument to 1 to see the console of the launched client
    pathtoexec = "/Users/javiermorenovega/GitHub/RA-practica1-vrep/client.py"
    -- pathtoexec = "/home/jmorenov/git/RA-practica1-vrep/client.py"
    args = portNb.." "..robot.." "..leftMotor.." "..rightMotor.." "..sensors
    result = simLaunchExecutable(pathtoexec, args, 1) -- set the last argument to 1 to see the console of the launched client
    if (result == -1) then
        -- The executable could not be launched!
        simDisplayDialog('Error',"Remote client could not be launched. &&nSimulation will not run properly",sim_dlgstyle_ok,true,nil,{0.8,0,0,0,0,0},{0.5,0,0,1,1,1})
    end
end