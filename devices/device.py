from .devices_status_db import DevicesStatusDB

class Device:
    def parse(self, jsonObj):
        self.id = jsonObj['id']
        self.name = jsonObj['name']
        self.type = jsonObj['type']
        self.location = jsonObj['location']

        self.allstatus = {}
        for s in jsonObj['status']:
            self.allstatus[s['name']] = s['type']

        return

    def get_status_type(self, statusname):
        """
        Get the type of a particular status
        """
        if statusname in self.allstatus:
            return self.allstatus['statusname']
        
        return None

    def get_status_value(self, statusname):
        if not statusname in self.allstatus:
            return None

        db = DevicesStatusDB.default_instance()
        return db.get_value(self.name, statusname)
    
    def get_device_name(self):
        return self.name
