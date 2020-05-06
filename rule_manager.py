import os
import tempfile

"""Rule Manager
Manage rule sets.
Output to a single rule file.

The class will maintain a list of current activated rule files.
When generating output, the content of the files will be copied to the output file.
The sequence of output is not guaranteed.
"""
class RuleManager:
    def __init__(self, output_destination, query_rule_by_id_callback, keep_original_content=False):
        """
        Inputs:
            output_destination: A path to output rule file.
                The file will be changed during runtime.
                All the original content will be kept/wipped based on keep_original_content.
            query_rule_by_id_callback:
                A function that allows query rule by id.
                rule=function(id)
            keep_original_content: Keep the original content of the output file.
                The original content will be at the begining of the file, and all additional content
                will be appended.
                If the file doesn't exist, no error will be thrown.
        """
        self.output_destination = output_destination
        self.query_rule_by_id_callback = query_rule_by_id_callback
        # set of activated id
        self.rules = set()
        # save original content if needed
        self.keep_original_content = keep_original_content
        self.original_content = ''
        if keep_original_content and os.path.exists(output_destination):
            try:
                with open(output_destination, 'r') as of:
                    self.original_content = of.read()
            except:
                print(f'[Info] Cannot read {output_destination} to save original content. Ignoring.')

    def add_rules(self, list_of_id):
        """
        Add pathes to rule into activated rule set.
        Inputs:
            list_of_id: A list of policy id.
                The content of the rule files will be copied directly.

        Returns:
            A integer number means the number of rules got added.
        """
        ret = 0
        for rfp in list_of_id:
            if rfp not in self.rules:
                ret += 1
                self.rules.add(rfp)

        return ret

    def remove_rules(self, list_of_id):
        """
        Remove pathes to rule from activated rule set.
        Inputs:
            list_of_id: A list of pathes to rule files.
            The path will be remove from activated rule set.

        Returns:
            A integer number means number of rules removed.
        """
        ret = 0
        for rfp in list_of_id:
            if rfp in self.rules:
                ret += 1
                self.rules.remove(rfp)

        return ret

    def clear_rules(self):
        """
        Remove all activated rules.
        """
        self.rules = set()

    def get_activated_id(self):
        """
        Get a set of activated ids.
        Returns:
            A set of id.
        """
        return self.rules

    def generate_output(self):
        """
        Generate output.
        Read the content of the files in the activated rule set and copy them into the output file.
        The original content of the output file will be kept/wipped based on setting.
        """
        # output to a tempfile first just in case something goes wrong
        # if something really goes wrong, don't change the output file
        tf = tempfile.TemporaryFile('w+')
        removed_policy = []
        # put the original content first
        if self.keep_original_content:
            print(self.original_content, file=tf)
        # output rules
        for rfp in self.rules:
            rule = self.query_rule_by_id_callback(rfp)
            if rule is None:
                removed_policy.append(rfp)
                continue
            with open(rule, 'r') as rf:
                tmp = rf.read()
                print(tmp, file=tf)

        # output to actual output file
        # rewind tempfile and copy line by line
        tf.seek(0)
        with open(self.output_destination, 'w') as of:
            for line in tf:
                print(line.rstrip(), file=of)
        tf.close()

        # handle removed policies
        self.remove_rules(removed_policy)
