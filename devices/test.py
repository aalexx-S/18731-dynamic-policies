from .devices_manager import DevicesManager

def device_changed(dev, status, value):
    print('Received status update of ' + dev + '.' + status + '=' + value)

if __name__ == "__main__" :
    devmgr = DevicesManager()
    devmgr.start(device_changed)

    motiondev = devmgr.find_devices('HomeMotion')
    if motiondev:
        print(motiondev.get_all_status())

    devmgr.wait()
