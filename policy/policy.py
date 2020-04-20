
"""A policy entry
"""
class Policy:
    def __init__(self, condition, action, rule, idd=None):
        self.__condition = condition
        self.__action = action
        self.__rule = rule
        self.idd = idd

    """Exceptions:
    TypeError:
        The final evaluation result is not a boolean.
    """
    def evaluate(self):
        re = self.__condition.evaluate()
        if not isinstance(re, bool):
            raise TypeError('The evaluation result is not a boolean. Got {0}.'.format(re))
        return re

    @ property
    def used_name(self):
        return self.__condition.used_name

    @ property
    def rule(self):
        return self.__rule

    @ property
    def action(self):
        return self.__action

    @property
    def id(self):
        return self.idd

    def __str__(self):
        return '{' + '"condition": {0}, "rule": "{1}", "action": "{2}"'.format(self.__condition.__str__(), self.rule, self.action) + '}'
