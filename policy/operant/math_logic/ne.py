import math

def operate(a, b):
    if isinstance(a, float) or isinstance(b, float):
        return not math.isclose(a, b)
    return a != b
