from .operant_binary import parse as parse_bin
from .operant_logic import parse as parse_logic
from .operant_constant import accept_types as constant_types
from .operant_constant import parse as parse_constant
from .operant_device import parse as parse_device

"""Return operator based on input json object
The json object must follow input policy format
Inputs:
    json_obj: A json_obj stores input json token.
    query_device_handle: a function allows query device data with name.
Returns:
    1. Operant object.
    2. Used device data name.
"""
def parse(json_obj, query_device_handle):
    # check type
    if 'type' not in json_obj:
        raise ValueError('"type" field not found in the given json object: ' + json_obj.__str__())

    if json_obj['type'] == 'bin':
        return parse_bin(json_obj), None

    if json_obj['type'] == 'logic':
        return parse_logic(json_obj), None

    if json_obj['type'] in constant_types:
        return parse_constant(json_obj), None

    if json_obj['type'] == 'device':
        re = parse_device(json_obj, query_device_handle)
        return re, re.name

    raise ValueError('Unknown type for token: ' + json_obj.__str__())
