from .operant import Operant

class Operant_constant(Operant):
    def __init__(self, value, vtype):
        self.opname = '{0}:{1}'.format(vtype, value)
        self.value = value

    def operate(self, input_list):
        return self.value


accept_types = ['int', 'float', 'boolean', 'bool', 'string']

def parse(json_obj):
    # check value
    if 'value' not in json_obj:
        raise ValueError('"value" field not found in given json object: ' + json_obj.__str__())

    if json_obj['type'] == 'int':
        return Operant_constant(int(json_obj['value']), 'int')
    if json_obj['type'] == 'float':
        return Operant_constant(float(json_obj['value']), 'float')
    if json_obj['type'] == 'boolean' or json_obj['type'] == 'bool':
        if json_obj['value'] == 'true':
            return Operant_constant(True, 'boolean')
        if json_obj['value'] == 'false':
            return Operant_constant(False, 'boolean')
        raise ValueError('Only accept "true" and "false" for boolean but get {0} instead.'.format(json_obj['value']))
    if json_obj['type'] == 'string':
        return Operant_constant(json_obj['value'], 'string')
    raise ValueError('Unknown handled constant type: ' + json_obj['type'])
