# API

## DeviceManager
DevicesManager.start(callback)
- Use it to start devices manager at the initialization phase of the program
- param: callback
  - Function callback to receive notification when a device status updated.
  - Signature: callback(device_name, status_name, value)
- no return

DevicesManager.findDevices(devname)
- Find the device of the particular name
- param: devname
  - name of the device to look up
- return: Device object if found, None otherwise

## Device
get_status(status_name)
- Get a particular status of a device
- param: status_name
  - name of the status to retrieve
- return: value of the status

