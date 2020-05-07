
"""Binary operant OR
perform OR on two inputs.
Allow short cut if the result is True.
"""
def operate(a, b):
    if a or b:
        return True, True
    return False, False
