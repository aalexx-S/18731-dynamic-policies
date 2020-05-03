
"""Binary operant AND.
Perform AND on two input values.
Allow short cut when result is False.
"""
def operate(a, b):
    if a is None:
        if b:
            return False, True
        return True, False
    if not a or not b:
        return True, False
    return False, True
