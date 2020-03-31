from devices_status_db import DevicesStatusDB

class Device:
    def __init__(self, id, name, type, location):
        self.id = id
        self.name = name
        self.type = type
        self.location = location
        return

    def get_status(self, statusname):
        db = DevicesStatusDB.getInstance()
        return db.get_value(self.name, statusname)
