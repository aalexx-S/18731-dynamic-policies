
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

### FIFO Manager

A simple FIFO management.

It implements a blocking reading, and a blocking writing with optional timeout.

It requires a path to a fifo to initilize. The fifo doesn't need to be there, the class will create it when initilized.

Notice that fifos are strictly uni-directional.

#### Init

```python
from fifo_manager import FIFOManager
```

Open for read:

```python
fm = FIFOManager('fifofile1', 'r')
```

Open for write:

```python
fm = FIFOManager('fifofile1', 'w')
```

Notice that this only initilize the instance. It won't open the fifo.

#### Read from fifo

Call ```read()``` function. It will be blocked until the writer closes the fifo. 

```python
read_string = fm.read()
```

To listen to the fifo continuously, you can add a while true loop around it:

```python
while True:
	read_string = fm.read()
	do_something(read_string)
```

#### Write to fifo

Call ```write()``` function. It will block until it has a reader.

```python
fm.write('some string')
```

You might want to add a timeout.

The function will return after timeout seconds, and it will abort its pending writing.

For example, adding a 5 seconds timeout.

```python
fm.write('some string', 5)
```
