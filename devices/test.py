from .devices_manager import DevicesManager

def device_changed(dev, status, value):
    print('Received status update of ' + dev + '.' + status + '=' + value)

if __name__ == "__main__" :
    devmgr = DevicesManager()
    devmgr.start(device_changed, statusport = '8080', redishost='127.0.0.1')
  
    print(devmgr.get_all_devices())

    motiondev = devmgr.find_devices('HomeMotion')
    if motiondev:
        print(motiondev.list_status())
        print(motiondev.get_all_status())
        
    stovedev = devmgr.find_devices('Stove1')
    if stovedev:
        print(stovedev.get_all_status())

    for status_name in stovedev.list_status():
            print(stovedev.get_status_value(status_name))
    try:
        devmgr.wait()
    except KeyboardInterrupt:
        print('receive Ctrl-C')
        devmgr.stop()
