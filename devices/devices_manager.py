from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import threading
from .device import Device
from .devices_status_db import DevicesStatusDB
import os

"""
Main components for managing devices. Called DevicesManager.start() in initialization
"""
class DevicesManager:
    def __init__(self):
        self.alldevs = {}
        self.monitor_thread = None

    def start(self, status_callback = None, dev_path = '', redishost = 'redis', redisport = '6379'):
        """
        Call this function to initialize device manager. This function will 
        read in all available devices and start the HTTP server to monitor
        device status.
        :param function status_callback: callback function to receive device update notification
        :param string dev_path: file path that contains list of all devices.
        """
        mydir = os.path.dirname(os.path.abspath(__file__))
        if not dev_path:
            dev_path = os.path.join(mydir, 'devices.json')

        with open(dev_path) as f:
            devData = json.load(f)
            assert devData is not None
            for name in devData:
                newdev = Device()
                newdev.parse(devData[name])
                # name = newdev.get_device_name()
                self.alldevs[name] = newdev

        db = DevicesStatusDB(redishost, redisport)
        DevicesStatusDB.set_default(db)

        # Create a thread to bring up an HTTP server for devices status monitor
        self.monitor_thread = _DevicesMonitor.start(self, status_callback)
        return
    
    def wait(self):
        if self.monitor_thread is not None:
            self.monitor_thread.join()
        return
    
    def find_devices(self, devname):
        """
        Policy server could use this function to retrieve a device and get its
        status.
        :return Device: The device object
        """
        if not devname in self.alldevs:
            return None

        return self.alldevs[devname]
    
    def get_all_devices():
        return list(self.alldevs.values())


class _DevicesMonitor:
    """
    Simulate the interface that receive updated status from devices.
    """

    callback = None
    devManager = None

    class DeviceThread(threading.Thread):
        def run(self):
            server_address = ("localhost", 8080)
            handler_class = _MyHandler
            server_class = HTTPServer

            httpd = HTTPServer(server_address, handler_class)
            print("server running...")

            try: 
                httpd.serve_forever()
            except KeyboardInterrupt: pass

            httpd.server_close()

    
    @staticmethod
    def start(manager, cb):
        assert manager is not None
        _DevicesMonitor.callback = cb
        _DevicesMonitor.devManager = manager
        dev_thread = _DevicesMonitor.DeviceThread()
        dev_thread.start()

        return dev_thread

    @staticmethod
    def update_status(devname, status, value):
        # from devices_manager import DevicesManager
        if _DevicesMonitor.devManager.find_devices(devname) is None:
            print('device %s not exist' % (devname))
            return
        
        db = DevicesStatusDB.default_instance()
        db.set_status(devname, status, value)
        if _DevicesMonitor.callback is not None:
            _DevicesMonitor.callback(devname, status, value)
    

class _MyHandler(BaseHTTPRequestHandler):
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        # # example: this is how you get path and command
        # print(self.path)
        # print(self.command)

        q_part = parse_qs(urlparse(self.path).query)

        if 'device' in q_part and 'status_name' in q_part \
            and 'status_value' in q_part:
            device = q_part['device'][0]
            status_name = q_part['status_name'][0]
            status_value = q_part['status_value'][0]

            print('device=%s status_name=%s status_value=%s' % (device, status_name, status_value))
            _DevicesMonitor.update_status(device, status_name, status_value)
            self._set_response(200)
            return

        self._set_response(400)

    def do_POST(self):
        self._set_response(405)

    def do_DELETE(self):
        self._set_response(405)
