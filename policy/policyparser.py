import json
from collections import defaultdict

from .conditiontoken import ConditionToken
from .policy import Policy

"""PolicyParser
Parse policies in a file to policy objects.
Also extract a few information for latter uses.
"""
class PolicyParser:
    """Parse policy file into Policy objects.
    Input:
        policyfile: A string for path to policy file.
        query_device_handle: a function for query device data with a string
            Signature: function(string)
            Should return a value representing the query result.
    """
    def __init__(self, policyfile, query_device_handle):
        self.policyfile = policyfile
        self.query_device_handle = query_device_handle
        # stores mapping from device data name to policies
        self.__name = defaultdict(list)
        # stores all conditions
        self.__conditions = []

    """The actual init function
    seperate this from object creation to enable parallelize
    Exceptions:
        FileNotFoundError: input file not found..
    """
    def initialize(self):
        try:
            pf = open(self.policyfile)
            p = json.load(pf)
        except FileNotFoundError:
            raise FileNotFoundError('Input file not exists: {0}'.format(self.policyfile))

        # parse conditions
        for c in p:
            cond = ConditionToken(c['condition'], self.query_device_handle)
            act = 'activate'
            if 'action' in c:
                act = c['action']
                if act != 'activate' and act != 'deactivate':
                    raise ValueError('Invalide action. Expect "activate" or "deactivate" but got {0} instead.'.format(act))
            rule = c['rule']

            policy = Policy(cond, act, rule)
            self.add_policy(policy)

        pf.close()

    def add_policy(self, policy):
        self.__conditions.append(policy)
        for name in policy.used_name:
            self.__name[name].append(policy)

    def query_policy_by_data_name(self, name):
        return self.__name[name]

    @ property
    def policies(self):
        return self.__conditions

    def __str__(self):
        if len(self.policies) == 0:
            return '[]'
        re = '[' + self.policies[0].__str__()
        for p in self.policies[1:]:
            re += ', ' + p.__str__()
        return re + ']'
