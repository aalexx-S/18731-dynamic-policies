from .devices_status_db import DevicesStatusDB

class DeviceStatus:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.value = 0

    def __repr__(self):
        return ('DeviceStatus: %s %s = ' % (self.type, self.name)) + str(self.value)

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
            return self.allstatus[statusname]
        
        return None

    def get_status_value(self, statusname):
        """
        Get the value of a status, the returned value will be type-casted to the 
        status type.
        :param string statusname: name of the status
        :return: status value if found, None otherwise
        """
        if not statusname in self.allstatus:
            return None

        db = DevicesStatusDB.default_instance()
        value = db.get_status(self.name, statusname)
        if not value:
            return None

        stype = self.get_status_type(statusname)
        if stype is None:
            return None
        
        stype = stype.lower()

        typed_value = None
        try:
            if stype == 'boolean':
                if value.lower() == 'true':
                    typed_value = True
                else:
                    typed_value = False
            elif stype == 'float':
                typed_value = float(value)
            elif stype == 'int':
                typed_value = int(value)
            elif stype == 'string':
                typed_value = value
            else:
                print('unknown status type %s' % (stype))
        except ValueError:
            print('Type casting %s to type %s fail' % (value, stype))
        
        return typed_value
    
    def get_device_name(self):
        return self.name
    
    def list_status(self):
        return list(self.allstatus.keys())
    
    def get_all_status(self):
        result = []
        for k in self.allstatus:
            ds = DeviceStatus()
            ds.value = self.get_status_value(k)
            ds.name = k
            ds.type = self.allstatus[k]
            result.append(ds)
        return result
