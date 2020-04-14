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
        # stores id to policy mapping
        self.__id_to_policy = {}
        self.__next_id = 0

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
                    raise ValueError('Invalid action. Expecting "activate" or "deactivate" but get {0} instead.'.format(act))
            rule = c['rule']

            policy = Policy(cond, act, rule, self.__next_id)
            self.__next_id += 1
            self.add_policy(policy)

        pf.close()

    def add_policy(self, policy):
        self.__conditions.append(policy)

        for name in policy.used_name:
            self.__name[name].append(policy)

        self.__id_to_policy[policy.id] = policy

    def query_policy_by_data_name(self, name):
        # check if policy is removed
        tmp = []
        for p in self.__name[name]:
            if p.id in self.__id_to_policy:
                tmp.append(p)
        self.__name[name] = tmp

        return tmp

    def query_policy_by_id(self, target_id):
        if target_id not in self.__id_to_policy:
            return None
        return self.__id_to_policy[target_id]

    @property
    def policies(self):
        return self.__conditions

    def __str__(self):
        if len(self.policies) == 0:
            return '[]'
        re = '[' + self.policies[0].__str__()
        for p in self.policies[1:]:
            re += ', ' + p.__str__()
        return re + ']'
