# Policy

## Policy Formats

This format isn’t designed for good readability.

It is designed for clear logic for the program input.

See explanation below for the definition of "token" and the spec of fields.

```json
[
  {
	"condition": {
      "type" : "type of token",
      "op": "type of operator",
      "input": [
      ],
      "value": "A string of value"
    },
    "action": "activate or deactivate",
    "rule": "path to rule file"
  }
]
```

- A input file contains a list of condition-rule dictionaries.

- A condition always starts with a single dictionary called "token".

- "Input" field is a list of input tokens.

- Only "type" is required for each token, other fields may be required based on the value of "type".

- The name for device data should always be formatted like "device\_name.data\_name"("device name"[dot]"data name").  

### Specs

- "condition": Any dictionary in condition is called a "token".

	A token must contain a "type" field.

	A condition is met if and only if the evaluation result is true.

	If the evaluation result is not a boolean, it will throw a TypeError during evaluation.

- "type":

	- "bin": Look into the value in the "op" field.

		"op" field must be a binary operator: "AND", "OR", "NOT"

		- "AND", "OR": Perform binary logic "and" and "or" to the list of input tokens.

		- "NOT": Perform binary logic "not". Only accept one token from the input list.

		There should only be exactly one token in the input list.

	- "logic": Look into the value in the "op" field.

		"op" field must be an equality logic: "==", "!=", ">", "<", ">=", "<="

		Perform the logic on two tokens from the input list.

		The evaluation is done in this specific order: token[0] operator token[1].

		The return value is always a boolean.

		There should only be exactly two tokens in the input list.

	- "int": Format the string in "value" field into int and return it.

	- "float": Format the string in "value" field into float and return it.

		- All equality checks will use ```math.isclose``` if one of the inputs is a float.

	- "boolean": Format the string in the "value" field into boolean and return it.

		Only accept strings: "true" and "false".

	- "string": Keep the string in the "value" field and return it.

	- "device": Keep the string in "value" field. The string represents a device data’s name.

		The name will be used to query data from the database module directly.

		Further processing to the string or not is up to the database module.


- "rule": A string representing a path to a file.

  This value will be stored and returned directly.

  Validating and reading the path is up to the execution engine.

  The structure used to store and evaluate logics will not handle these jobs.

- "action": Either "activate" or "deactivate".

  Default to "activate" if not presented.

  It is up to the execution engine how to perform the actions.

## Usage

Import the object ```PolicyParser``` from ```policyparser```.

### Init

```python
someobj = PolicyParser('path/to/policyfile', query_device_handle)

someobj.initialize()
```
- query_device_handle: a function that allows query a device data by name.
    - Its signature should look like this: ```value = function(name)```.
        ```value``` is a single return value of a device data called ```name```.
    - The returned value from ```query_device_handle``` will be used directly.
        Make sure ```query_device_handle``` returns correct types of data.

### Access Parsed Policies

#### Access Policies

All the policies are stored in a list ```policies```.

The list can be access throguh ```policyparser_obj.policies```.

It is a list of ```Policy``` objects, so you can iterate through them.

#### Access Policies By Data Name

Use member function ```query_policy_by_data_name(name)``` to access a list of ```Policy``` objects that used the data ```name``` in their condition.

Return an empty list if there is not policy that use the data ```name```.

### Evaluate a Policy

Call ```evaluate()``` member function for a policy object to evaluate a boolean result during runtime.

### Get Rule of a Policy

Use ```rule``` attribute of a policy object to access its rule.

This will return a path to the rule file.

### Get Action of a Policy

Use ```action``` attribute of a policy object to access its action.

The action value is either 'activate' or 'deactivate'.

Default to 'activate' if not given in policy file.

### Debug

I implemented \_\_str\_\_() for the objects, so you can print them with normal ```print``` on ```PolicyParser``` and ```Policy``` and all other objects.
