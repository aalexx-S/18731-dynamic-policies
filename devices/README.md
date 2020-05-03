# Overview
The intended usage: main function call the DevicesManager.start()
to initialize this module. After the initialization, the policy evaluator
could call findDevices() or get_all_devices() to retrieve device object and 
then check the status of those devices.

# Spec
Possible device status type name (should be same as policy value):
- boolean
- int
- float
- string

# API

## DeviceManager
DevicesManager.start(callback)
- Use it to start devices manager at the initialization phase of the program
- param: (see function comment for details.)
- no return

DevicesManager.stop()
- Stop the device manager during cleanup
- no return

DevicesManager.findDevices(devname)
- Find the device of the particular name
- param: 
  - (String) devname: name of the device to look up
- return: Device object if found, None otherwise

DevicesManager.get_all_devices()
- Get all devices available in the system
- return: a list of Device object

## Device
get_status_type(statusname)
- Get the type of a status
- param: 
  - (String) statusname: name of the status to retrieve
- return (String) : type of the status

get_status_value(statusname)
- Get the value of a status
- param:
  - (String) statusname: name of the status to retrieve
- return (String) : value of the status

get_device_name()
- Get name of the device
- return (String): name of the device

list_status()
- Get all possible status name of the device
- return (List): list of status name in string

get_all_status()
- Get a list of DeviceStatus object
- param: status_name
  - name of the status to retrieve
- return (List): a list of DeviceStatus object. The status object contains the name, type and value of the status

# Simulate device status update
Use this command to update device status
`wget "http://localhost:8080/?device=<deviceName>&status_name=<statusName>&status_value=<statusValue>"`

Three params (Refer to devices.json of valid value to these fields)
- device
- status_name
- status_value