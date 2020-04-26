
"""A policy entry
"""
class Policy:
    def __init__(self, condition, action, rule, idd=None):
        """
        Policy object. Containing condition, action and rule.
        Parameter:
            condition:
                A condition token.
            Action:
                'activate' or 'deactivate'.
            rule:
                A path to rule file.
            idd:
                Id of the policy. This will be auto assigned when adding policies to policyparser.
                None by default.
        """
        self.__condition = condition
        self.__action = action
        self.__rule = rule
        self.__idd = idd

    """Exceptions:
    TypeError:
        The final evaluation result is not a boolean.
    """
    def evaluate(self):
        re = False
        try:
            re = self.__condition.evaluate()
        except Exception as e:
            # on exception, set evaluation result to False
            print('Warning, exception caught when evaluating. Return false.')
            print(e)
            return False

        if not isinstance(re, bool):
            print(f'Warning, the evaluation result is not a boolean. Got {re}. Return false.')
            return False
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
        return self.__idd

    def _set_id(self, idd):
        """
        This is a non-public method.
        Don't use this unless you know what you are doing.
        There are some other classes relies on id.
        """
        self.__idd = idd

    def __repr__(self):
        return f'Policy(id={self.id}, rule={self.rule})'

    def __str__(self):
        return '{' + '"condition": {0}, "rule": "{1}", "action": "{2}"'.format(self.__condition.__str__(), self.rule, self.action) + '}'
