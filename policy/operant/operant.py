
"""Base operant
Base operant object.
Implements a null behavior.
"""
class Operant:
    def operate(self, input_list):
        return None

    def __str__(self):
        return "{0}".format(self.opname)
