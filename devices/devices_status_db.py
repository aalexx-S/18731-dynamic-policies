import redis

class DevicesStatusDB:
    __instance = None

    @staticmethod
    def default_instance():
        """ Static access method. """
        if DevicesStatusDB.__instance == None:
            raise Exception('No default instance found, please call a constructor first!')
        
        return DevicesStatusDB.__instance

    @staticmethod
    def set_default(inst):
        assert isinstance(inst, DevicesStatusDB)

        DevicesStatusDB.__instance = inst


    def __init__(self, host='redis', port='6379'):
        self.r = redis.Redis(host=host, port=port)
        if DevicesStatusDB.__instance == None:
            __instance = self
        
        return

    def get_status(self, dev, name):
        key = dev + '.' + name
        return self.r.get(key)

    def set_status(self, dev, name, value):
        key = dev + '.' + name
        self.r.set(key, value)

