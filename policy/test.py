import sys
# sys.path.insert(1, '/home/ubuntu/18731-dynamic-policies/policy')
from policyparser import *
someobj = PolicyParser('/home/ubuntu/18731-dynamic-policies/policy/example_policy.json', query_device_handle)

someobj.initialize()

print(policies)