from .operant import parser as op_parser

# Condition parsing and evaluation
class ConditionToken:
    """Init and parse condition from a json object
    Input:
        json_obj:
            A json object following policy file format
        query_device_handle:
            A function the allows query device data with name.
            Signature: value = function(string).
    """
    def __init__(self, json_obj, query_device_handle):
        self.query_device_handle = query_device_handle
        self.__used_name = set() # a list of used device data name, save for latter uses

        # parse operant from json object
        self.action, device_name = op_parser.parse(json_obj, query_device_handle)

        if device_name:
            self.__used_name.add(device_name)

        # recursive parse input tokens if needed
        self.input_tokens = []
        if 'input' in json_obj:
            for t in json_obj['input']:
                tc = ConditionToken(t, query_device_handle)
                self.input_tokens.append(tc)
                self.__used_name.update(tc.used_name)
                tc.remove_used_names()

    def evaluate(self):
        try:
            return self.action.operate(self.input_tokens)
        except ValueError:
            raise

    @ property
    def used_name(self):
        return self.__used_name

    def remove_used_names(self):
        # erase remembered used device data name
        self.__used_name = set()

    def __str__(self):
        re = '{' + '"operant": "{0}"'.format(self.action.__str__())
        if self.input_tokens:
            re += ', "input": ['
            re += self.input_tokens[0].__str__()
            for i in self.input_tokens[1:]:
                re += ', ' + i.__str__()
            re += ']'
        return re + '}'
