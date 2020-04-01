import sys
# sys.path.insert(1, '/home/ubuntu/18731-dynamic-policies/policy')
from policy.policyparser import *

def hola():
    return ""

someobj = PolicyParser('/home/ubuntu/18731-dynamic-policies/policy/example_policy.json', hola)

someobj.initialize()

print(someobj.policies)