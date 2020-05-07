from .operant import Operant

class Operant_device(Operant):
    def __init__(self, name, query_device_handle):
        self.__name = name
        self.query_device_handle = query_device_handle
        self.opname = 'device:{0}'.format(name)

    def operate(self, input_list):
        return self.query_device_handle(self.name)

    @ property
    def name(self):
        return self.__name

def parse(json_obj, query_device_handle):
    return Operant_device(json_obj['value'], query_device_handle)
