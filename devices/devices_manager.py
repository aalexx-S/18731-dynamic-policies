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

    def start(self, status_callback = None, dev_path = '', redishost = 'redis', redisport = '6379', statusport = None):
        """
        Call this function to initialize device manager. This function will 
        read in all available devices and start the HTTP server to monitor
        device status.
        :param function status_callback: callback function to receive device update notification
        :param string dev_path: file path that contains list of all devices.
        :param string redishost: hostname of redis server
        :param string redisport: port of redis server
        :param string statusport: the port of http server to receive device update, 
            the server wil not be started if caller do not provide port
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
                self.alldevs[name] = newdev

        db = DevicesStatusDB(redishost, redisport)
        DevicesStatusDB.set_default(db)

        # Create a thread to bring up an HTTP server for devices status monitor
        if statusport is not None:
            self.monitor_thread = _DevicesMonitor.start(self, status_callback, int(statusport))
        return
    
    def stop(self):
        _DevicesMonitor.stop()
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
    
    def get_all_devices(self):
        return list(self.alldevs.values())


class _DevicesMonitor:
    """
    Simulate the interface that receive updated status from devices.
    """

    callback = None
    devManager = None
    httpd = None

    class DeviceThread(threading.Thread):
        
        def __init__(self, port):
            super().__init__()
            self.port = port

        def run(self):
            server_address = ("localhost", self.port)
            handler_class = _MyHandler
            server_class = HTTPServer

            _DevicesMonitor.httpd = HTTPServer(server_address, handler_class)
            print("server running...")

            try: 
                _DevicesMonitor.httpd.serve_forever()
            except KeyboardInterrupt: 
                pass

            _DevicesMonitor.httpd.server_close()

    
    @staticmethod
    def start(manager, cb, statusport):
        assert manager is not None
        _DevicesMonitor.callback = cb
        _DevicesMonitor.devManager = manager
        dev_thread = _DevicesMonitor.DeviceThread(statusport)
        dev_thread.start()

        return dev_thread

    @staticmethod
    def stop():
        if _DevicesMonitor.httpd != None:
            _DevicesMonitor.httpd.shutdown()
            _DevicesMonitor.httpd = None

    @staticmethod
    def update_status(devname, status, value):
        dev = _DevicesMonitor.devManager.find_devices(devname)
        if dev is None:
            print('device %s not exist' % (devname))
            return
        
        stype = dev.get_status_type(status)
        if stype is None:
            print('status_name %s not exist' % (status))
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
