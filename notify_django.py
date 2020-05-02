import json

from fifo_manager import FIFOManager

def notify_django(runtime):
    """
    Construct evaluation result message and notify django server the evaluation result.
    Parameters:
        runtime:
            A namespace that stores a policy parser instance, a rule manager instance and a err_policy dict.
            Required name:
                policy_parser
                rule_manager
                err_policy
    """
    policyparser = runtime.policy_parser
    rm = runtime.rule_manager

    # construct message
    tmp = []
    tmps = set()
    for i in rm.get_activated_id():
        tmpd = {'id': f'{i}', 'status': 'activate'}
        tmp.append(tmpd)
        tmps.add(i)
    for i in runtime.err_policy.keys():
        tmpd = {'id': f'{i}', 'status': 'error'}
        tmp.append(tmpd)
        tmps.add(i)
    for p in policyparser.policies:
        if p.id not in tmps:
            tmpd = {'id': f'{p.id}', 'status': 'deactivate'}
            tmp.append(tmpd)

    # sort the ids
    tmp = sorted(tmp, key=lambda x: x['id'])

    message = json.dumps({'rules': tmp})

    fm = FIFOManager('E2D', 'w')
    fm.write(message, 3)
