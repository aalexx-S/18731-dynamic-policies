
# Test Redis
1. Run `docker-compose up` to bring up server and redis Docker
2. Run `docker exec -t -i 18731-dynamic-policies_redis_1 /bin/bash` to connect to redis server
3. Run `redis-cli`

# Dynamic Policies

## Usage

Use ```python3 main.py -h``` for help.

```
python3 main.py config.json
```

Please refer to ```example_config.json```.
All fields must exist.

The program will run forever until it receives sigint.

It will enter cleanup process after receiving the first sigint, and it will be killed brutefully by the second sigint.

Add ```--debug``` flag to print stderr, otherwise all stderr messages are dumped to devnull.


## Modules

### Rule Manager

A simple class that manage current activated rules.

It requres a path to a output file.

Add and remove rules by calling ```add_rules``` and ```remove_rules``` with a list of policy id.

Update the output file by calling ```generate_output``` function.

Example usage:

```python
from rule_manager import RuleManager

rule_manager = RuleManager('path_to_output', query_rule_by_id_handle)

rule_manager.add_rules(['0', '2', '3'])

rule_manager.remove_rules(['2'])

rule_manager.generate_output()
```

```query_rule_by_id_handle``` is a function that allows rule manager to query path to rule file by policy id.

By default, the original content in the output file will be wiped out.

Pass ```True``` at object construction to keep the original content in the output file.

```python
rule_manager = RuleManager('path_to_output', query_rule_by_id_handle, True)
```

You can get all activated policy id by calling ```get_activated_id``` function.

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
