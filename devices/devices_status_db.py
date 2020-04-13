import redis

class DevicesStatusDB:
    __instance = None
    def __init__(self):
        if DevicesStatusDB.__instance != None:
            raise Exception("Use getInstance()!")
        
        DevicesStatusDB.__instance = self
        self.r = redis.Redis(host='redis', port='6379')

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DevicesStatusDB.__instance == None:
            DevicesStatusDB()
        return DevicesStatusDB.__instance

    def get_status(self, dev, name):
        key = dev + '.' + name
        return self.r.get(key)

    def set_status(self, dev, name, value):
        key = dev + '.' + name
        self.r.set(key, value)

