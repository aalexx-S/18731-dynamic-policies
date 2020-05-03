import argparse
import json
import os
import signal
import sys
import time
from functools import partial
from threading import Thread

from fifo_manager import FIFOManager
from rule_manager import RuleManager
from devices.devices_manager import DevicesManager
from policy.policyparser import PolicyParser
from runtime_evaluate_policy import evaluate_all, evaluate_policies
from endless_listen_from_django import EndlessListener
from notify_django import notify_django

def query_rule_by_id(runtime, idd):
    """
    Query rule by policy id.
    Parameters:
        runtime:
            A namespace that stores a policy parser instance.
            Required name:
                policy_parser
        idd:
            target id.
    Returns:
        A string to rule file, or None.
    """
    return runtime.policy_parser.query_policy_by_id(idd).rule

def query_device_handle(runtime, query_str):
    """
    Callback for policy parser.
    Use this to query device status.
    Parameters:
        runtime:
            A namespace that stores a devices manager instance.
            Required name:
                devices_manager
        query_str:
            a query string. Must follow the "device name"."status name" format.
    Returns:
        The result of query.
    """
    devices_manager = runtime.devices_manager
    dname, sname = query_str.split('.')

    dev = devices_manager.find_devices(dname)
    if dev is None:
        print(f'[Debug] Query {dname} from DevicesManager and got None.', file=sys.stderr)
        raise ValueError(f'Device {dname} not in database.')

    ret = dev.get_status_value(sname)
    if ret is None:
        print(f'[Debug] Query {dname}.{sname} from DevicesManager and got None.', file=sys.stderr)
        raise ValueError(f'Status {dname}.{sname} not in database.')

    return ret

def evaluate_policies_and_notify(runtime, dname, sname):
    evaluate_policies(runtime, dname, sname)
    notify_django(runtime)

def device_update_callback(runtime, dname, sname, _):
    """
    Callback function for device manager.
    Parameters:
        runtime:
            A namespace that stores a policy parser and rule manager instance
            Required name:
                policy_parser
                rule_manager
        dname:
            device name.
        sname:
            status name.
        value:
            value for that status.
    """
    # evaluate policies and notify the django server
    # use a separate thread so that it won't block caller
    th = Thread(target=evaluate_policies_and_notify, args=(runtime, dname, sname))
    th.start()

# global sigint flag
sigint_flag = False

def sigint_handler(signal_num, frame):
    global sigint_flag
    print("\n[Info] Enter cleanup process. Send sigint again to kill the program immediately.")
    # set sigint handler to system default, which is kill instead of raising exception.
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sigint_flag = True

#This is the main program of the system.
# It will initialize all the components.
# Then, It will run forever until receiving sigint.
def main(arg):
    """
    The main program.
    'arg' is the result from argparse.
    """
    config_json = None
    try:
        pf = open(arg.config, 'r')
        config_json = json.load(pf)
    except FileNotFoundError as e:
        raise
    pf.close()

    # check if print debug message
    if not arg.debug:
        # make sys.stderr point to dev null
        nf = os.open(os.devnull, os.O_RDWR)
        os.dup2(nf, 2)

    # initialize runtime namespace
    runtime = argparse.Namespace()

    # err policy dictionary. stores policy ids that can't be evaluated.
    runtime.err_policy = {}

    # initialize policyparser
    cb_p = partial(query_device_handle, runtime)
    pp = PolicyParser(config_json['policyfile'], cb_p)
    runtime.policy_parser = pp
    pp.initialize()

    # initialize rule manager
    cb_r = partial(query_rule_by_id, runtime)
    rm = RuleManager(config_json['output'], cb_r)
    runtime.rule_manager = rm

    # initialize database module
    dm = DevicesManager()
    runtime.devices_manager = dm
    cb_d = partial(device_update_callback, runtime)
    dm.start(cb_d, config_json['devicespec'], config_json['redisip'], config_json['redisport'], config_json['status_server_port'])

    # setup main thread
    listen_th = EndlessListener()
    listen_th.initialize(runtime, cb_p)
    listen_th.start()
    # register signal handler
    signal.signal(signal.SIGINT, sigint_handler)

    # do an initial evaluation with main thread
    # blocks main thread until finish evaluating
    evaluate_all(runtime)

    # wait for signal
    global sigint_flag
    while True:
        time.sleep(1)
        # handle signals and other events
        if sigint_flag:
            # cleanup
            # stop listening thread.
            listen_th.signal_stop()
            listen_th.join()
            # stop devices manager
            runtime.devices_manager.stop()
            break

    print("[Info] Main thread exit.")


if __name__ == "__main__":
    # Parse argument
    parser = argparse.ArgumentParser(description='Dynamic policy engine. The engine will run forever until killed.')
    parser.add_argument('config', help="Path to config file.")
    parser.add_argument('--debug', action='store_true', help='Print stderr message, otherwise stderr messages are nullified.')
    args = parser.parse_args()
    main(args)
