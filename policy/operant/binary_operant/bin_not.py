
"""Binary operant NOT
Perform NOT on the second input.
If the first input is not None, raise ValueError.

Always allow short cut
"""
def operate(a, b):
    if a is not None:
        raise ValueError("NOT only accept one argument, but two received.")
    return True, not b
