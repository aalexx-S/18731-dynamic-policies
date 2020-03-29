from .operant import Operant

from .math_logic import eq
from .math_logic import ne
from .math_logic import gt
from .math_logic import lt
from .math_logic import ge
from .math_logic import le

"""Math logic operant
Perform math logic on given two input tokens
"""
class Operant_logic(Operant):
    """Init
    Inputs:
        logicop: a math logic function.
        opname: a string name of the op.
    """
    def __init__(self, logicop, opname):
        self.logicop = logicop
        self.opname = opname

    def operate(self, input_list):
        if len(input_list) != 2:
            raise ValueError('Size of input list is not two for math logic. (got length={0})'.format(len(input_list)))
        return self.logicop(input_list[0].evaluate(), input_list[1].evaluate())


def parse(json_obj):
    # check op
    if 'op' not in json_obj:
        raise ValueError('"op" field not found in given json object: ' + json_obj.__str__())

    if json_obj['op'] == '==':
        return Operant_logic(eq.operate, '==')
    if json_obj['op'] == '!=':
        return Operant_logic(ne.operate, '!=')
    if json_obj['op'] == '>':
        return Operant_logic(gt.operate, '>')
    if json_obj['op'] == '<':
        return Operant_logic(lt.operate, '<')
    if json_obj['op'] == '>=':
        return Operant_logic(ge.operate, '>=')
    if json_obj['op'] == '<=':
        return Operant_logic(le.operate, '<=')
    raise ValueError('Unknown bin typed op: ' + json_obj['op'])
