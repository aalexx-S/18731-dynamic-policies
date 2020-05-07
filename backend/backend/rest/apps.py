from django.apps import AppConfig
import os
import sys

folder_path=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(folder_path, '..','..','..' ))
from devices.devices_manager import DevicesManager

def device_changed(dev, status, value):
    print('Received status update of ' + dev + '.' + status + '=' + value)

class RestConfig(AppConfig):
    name = 'rest'
    devmgr = DevicesManager()
    devmgr.start(device_changed, redishost='127.0.0.1')
