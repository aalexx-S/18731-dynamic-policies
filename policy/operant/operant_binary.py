from .operant import Operant

from .binary_operant import bin_and
from .binary_operant import bin_or
from .binary_operant import bin_not

"""Binary operant
Perform binary operator on a input list of tokens
"""
class Operant_binary(Operant):
    """Init
    Init with binary operant object
    Input:
        binop: A binary operant object
    """
    def __init__(self, binop, opname):
        self.binop = binop
        self.opname = opname

    def operate(self, input_list):
        if not input_list:
            raise ValueError("Input list size error.")
        short_cut, result = self.binop(None, input_list[0].evaluate())
        if short_cut:
            return result

        for item in input_list[1:]:
            short_cut, result = self.binop(result, item.evaluate())
            if short_cut is True:
                return result
        return result


def parse(json_obj):
    # check op
    if 'op' not in json_obj:
        raise ValueError('"op" field not found in given json object: ' + json_obj.__str__())

    if json_obj['op'] == 'AND':
        return Operant_binary(bin_and.operate, 'AND')
    if json_obj['op'] == 'OR':
        return Operant_binary(bin_or.operate, 'OR')
    if json_obj['op'] == 'NOT':
        return Operant_binary(bin_not.operate, 'NOT')
    raise ValueError('Unknown bin typed op: ' + json_obj['op'])
