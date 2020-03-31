import json
from device import Device
from devices_status_db import DevicesStatusDB

"""
Main components for managing devices. Called DevicesManager.start() in initialization
"""
class DevicesManager:
    alldevs = None
    
    @staticmethod
    def start(status_callback = None):
        # The devices.json serve as a database of available device now.
        with open('devices.json') as f:
            DevicesManager.alldevs = json.load(f)
            assert DevicesManager.alldevs is not None
        
        DevicesMonitor.set_callback(status_callback)
        return
    
    @staticmethod
    def find_devices(devname):
        """
        Policy server could use this function to retrieve a device and get its
        status.
        :return Device: The device object
        """
        if not devname in DevicesManager.alldevs:
            return None
        
        # TODO: create a thread to bring up an HTTP server for devices status monitor

        dev_obj = DevicesManager.alldevs[devname]
        return Device(dev_obj['id'], dev_obj['name'], dev_obj['type'], dev_obj['location'])


"""
Simulate the interface that receive updated status from devices.
"""
class DevicesMonitor:
    callback = None
    
    @staticmethod
    def set_callback(cb):
        DevicesMonitor.callback = cb

    @staticmethod
    def update_status(devname, status, value):
        # from devices_manager import DevicesManager
        if DevicesManager.find_devices(devname) is None:
            print('device %s not exist' % (devname))
            return
        
        db = DevicesStatusDB.getInstance()
        db.set_status(devname, status, value)
        if DevicesMonitor.callback is not None:
            DevicesMonitor.callback(devname, status, value)