from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import threading
from device import Device
from devices_status_db import DevicesStatusDB

"""
Main components for managing devices. Called DevicesManager.start() in initialization
"""
class DevicesManager:
    alldevs = None
    monitor_thread = None

    @staticmethod
    def start(status_callback = None):
        # The devices.json serve as a database of available device now.
        with open('devices.json') as f:
            DevicesManager.alldevs = json.load(f)
            assert DevicesManager.alldevs is not None
        
        # Create a thread to bring up an HTTP server for devices status monitor
        monitor_thread = DevicesMonitor.start(status_callback)
        return
    
    @staticmethod
    def wait():
        if DevicesManager.monitor_thread is not None:
            DevicesManager.monitor_thread.join()
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

        dev_obj = DevicesManager.alldevs[devname]
        return Device(dev_obj['id'], dev_obj['name'], dev_obj['type'], dev_obj['location'])


"""
Simulate the interface that receive updated status from devices.
"""
class DevicesMonitor:
    callback = None

    class DeviceThread(threading.Thread):
        def run(self):
            server_address = ("localhost", 8080)
            handler_class = MyHandler
            server_class = HTTPServer

            httpd = HTTPServer(server_address, handler_class)
            print("server running...")

            try: 
                httpd.serve_forever()
            except KeyboardInterrupt: pass

            httpd.server_close()

    
    @staticmethod
    def start(cb):
        DevicesMonitor.callback = cb
        dev_thread = DevicesMonitor.DeviceThread()
        dev_thread.start()
        return dev_thread

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
    

class MyHandler(BaseHTTPRequestHandler):
    def _set_response(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        # example: this is how you get path and command
        print(self.path)
        print(self.command)

        q_part = parse_qs(urlparse(self.path).query)

        if 'device' in q_part and 'status_name' in q_part \
            and 'status_value' in q_part:
            device = q_part['device'][0]
            status_name = q_part['status_name'][0]
            status_value = q_part['status_value'][0]

            print('device=%s status_name=%s status_value=%s' % (device, status_name, status_value))
            DevicesMonitor.update_status(device, status_name, status_value)
            self._set_response(200)
            return

        self._set_response(400)

    def do_POST(self):
        self._set_response(405)

    def do_DELETE(self):
        self._set_response(405)
