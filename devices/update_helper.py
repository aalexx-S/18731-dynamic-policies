import argparse
from devices_manager import DevicesManager, DevicesMonitor

# parse argument
parser = argparse.ArgumentParser(description='Update device status')
parser.add_argument('--dev', help='device name')
parser.add_argument('--status', help='status name')
parser.add_argument('--value', help='status value')
args = parser.parse_args()

def device_changed(dev, status, value):
    print('Received status update of ' + dev + '.' + status + '=' + value)

# TODO: change it to the function that receive events.
DevicesManager.start(device_changed)
DevicesMonitor.update_status(args.dev, args.status, args.value)
