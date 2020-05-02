import json
import threading

from fifo_manager import FIFOManager
from policy.policyparser import PolicyParser
from runtime_evaluate_policy import evaluate_all
from notify_django import notify_django

# endlessly listen to django's request until killed
# The program is meant to be a deamon process.
class EndlessListener(threading.Thread):
    def initialize(self, runtime, cb_p):
        """
        Parameters:
            runtime:
                A namespace that stores policy_parser and rule_manager
                Required name:
                    policy_parser
                    rule_manager
                    devices_manager
        """
        self.runtime = runtime
        self.cb_p = cb_p
        self.stop_flag = False
        self.FIFO_name = 'D2E'

    def signal_stop(self):
        self.stop_flag = True
        # Slightly touch the fifo to stop reading.
        # someone else may also be writing, use a timeout of 1 seconds
        FIFOManager(self.FIFO_name, 'w').write('', 1)

    def run(self):
        fm = FIFOManager(self.FIFO_name, 'r')
        while True:
            if self.stop_flag:
                break
            req = fm.read()
            if self.stop_flag:
                break

            req = json.loads(req)
            if req['task'] == 'upload_policy':
                new_pp = PolicyParser(req['path'], self.cb_p)
                new_pp.initialize()
                self.runtime.policy_parser = new_pp
                # reset rule manager
                self.runtime.rule_manager.clear_rules()
                # evaluate all policies for the new policy file
                # blocks main thread until finish evaluating
                evaluate_all(self.runtime)
                notify_django(self.runtime)
            elif req['task'] == 'query':
                notify_django(self.runtime)
