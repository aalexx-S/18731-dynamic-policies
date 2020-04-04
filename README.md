
# Test Redis
1. Run `docker-compose up` to bring up server and redis Docker
2. Run `docker exec -t -i 18731-dynamic-policies_redis_1 /bin/bash` to connect to redis server
3. Run `redis-cli`

# Dynamic Policies

## Usage

TODO

## Modules

### Rule Manager

A simple class that manage current activated rules.

It requres a path to a output file.

Add and remove rules by calling ```add_rules``` and ```remove_rules``` with a list of strings.

Update the output file by calling ```generate_output``` function.

Example usage:

```python
from rule_manager import RuleManager

rule_manager = RuleManager('path_to_output')

rule_manager.add_rules(['rule1', 'rule2', 'rule3'])

rule_manager.remove_rules(['rule2'])

rule_manager.generate_output()
```

By default, the original content in the output file will be wipped out.

Pass ```True``` at object construction to keep the original content in the output file.

```python
rule_manager = RuleManager('path_to_output', True)
```
