import logging
from threading import Thread

from notify_django import notify_django

def _evaluate_policy(runtime, policy):
    """
    Evaluate a single policy and make changes to rule manager.
    This function DOES NOT generate output.
    Parameters:
        runtime:
            A namespace that stores rule_manager instance and err_policy dictionary.
            Required name:
                rule_manager
                err_policy
        policy:
            The policy that is to be evaluated.
    """
    res = False
    # remove old exception for this policy
    if policy.id in runtime.err_policy:
        del runtime.err_policy[policy.id]

    try:
        res = policy.evaluate()
    except Exception as e:
        print(f'[Warn] Evaluation failed with exception: {str(e)}.')
        print(f'-- Current activation state of this policy will not be changed.')
        print(f'-- Current policy: {policy.__repr__()}.')
        runtime.err_policy[policy.id] = e
        return

    if res:
        act = (policy.action == 'activate')
    else:
        act = (policy.action == 'deactivate')

    if act:
        # activate rule
        runtime.rule_manager.add_rules([policy.id])
    else:
        # deactivate rule
        runtime.rule_manager.remove_rules([policy.id])

def evaluate_policies(runtime, dname, sname):
    """
    Evaluate policies and generate output.
    Inputs:
        runtime:
            A namespace that stores a policy parser instance and a rule manager instance.
            Required name:
                policy_parser
                rule_manager
        dname:
            device name.
        sname:
            status name.
    """
    policyparser = runtime.policy_parser
    rm = runtime.rule_manager
    # re-evaluate relative policies when status changes
    data = f'{dname}.{sname}'
    for p in policyparser.query_policy_by_data_name(data):
        _evaluate_policy(runtime, p)

    # generate output to specified output file
    try:
        rm.generate_output()
    except Exception as e:
        print(f'[Warn] Output generation failed with exception {str(e)}.')
        print(f'-- For safety purpose, the output file will not be changed.')

def evaluate_all(runtime):
    """
    Evaluate all policy stored in policyparser. Generate output afterward.
    Parameters:
        runtime:
            A namespace that stores a policyparser instance and a rule_manager instance.
            Required name:
                policy_parser
                rule_manager
    """
    policyparser = runtime.policy_parser
    for p in policyparser.policies:
        _evaluate_policy(runtime, p)

    # generate output to specified output file
    try:
        runtime.rule_manager.generate_output()
    except Exception as e:
        print(f'[Warn] Output generation failed with exception {str(e)}.')
        print(f'-- For safety purpose, the output file will not be changed.')
