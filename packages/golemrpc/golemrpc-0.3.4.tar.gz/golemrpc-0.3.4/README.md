# Overview 

Golemrpc is a python package allowing communication with a (remote) Golem node. Connection handling, golem task state handling, resources upload and results retrieval are handled automatically for the user. This package has been created mainly for RASPA2 use case, but it also works with basic blender rendering tasks (see examples). 

RASPA2 tasks are given to Golem in form of Python functions and `args` dictionary, e.g.:

```python
def raspa_task(args):
    '''Task to compute provider side.
    It is possible to import RASPA2 package on provider side because
    this package is preinstalled in a docker environment we are about
    to use (dockerhub golemfactory/glambda:1.3).
    '''
    import RASPA2
    import pybel

    mol = pybel.readstring('cif', args['mol'])

    return RASPA2.get_helium_void_fraction(mol)
```

It is called RASPA2 use case, however generic Python fuctions are equally acceptable. 

## Requirements

User must have access to Golem node (branch `glambda0.3`) with a public IP address and ports forwarded (e.g. AWS hosted). By access we mean 
SSL certificate and CLI secret files required for connection establishment.

## Installation

Use package installer for Python3:

```sh
pip3 install golemrpc==0.3.0
```

# User guide

## Basic example

First set up a logging module:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

Then create and start an RPCComponent:

```python
from golemrpc.rpccomponent import RPCComponent
rpc = RPCComponent(
    host='35.158.100.160',
    port=61000,
    cli_secret_filepath='golemcli_aws.tck',
    rpc_cert_filepath='rpc_cert_aws.pem'
)
rpc.start()
```

It will spawn a separate thread that will handle communication with Golem on `35.158.100.160:61000`. Now create a dummy task 
to compute on Golem provider's machine:

```python
def dummy_task(args):
    return 1 + args['b']
```

Create a golemrpc `CreateTask` [message](https://github.com/golemfactory/golemrpc/blob/threaded/docs/messages.md) with task type `GLambda`:

```python
message = {
    'type': 'CreateTask',
    'task': {
        'type': 'GLambda',
        'options': {
            'method': dummy_task,
            'args': {'b': 2},
        },
    }
}
```

and send it to RPCComponent. `GLambda` is an abbreviation for Golem Lambda. It is a type of task that takes serialized Python function and dictionary as input and sends them to the provider for computation.

```python
rpc.post(message)
```

Now poll the RPC message queue for [events](https://github.com/golemfactory/golemrpc/blob/threaded/docs/messages.md). First one we expect is `TaskCreatedEvent`:

```python
task_created_event = rpc.poll(timeout=None)
```

Second message coming from RPCComponent should be `TaskResults` containing filepaths to actual results:

```python
task_results = rpc.poll(timeout=None)
```

By default there are three files listed in `TaskResults` message: `result.json`, `stderr.log` and `stdout.log`. Result returned by `dummy_task` function is serialized to a `result.json` of form:

```json
{
    "data": 3,
}
```

If there are any errors in user supplied function JSON object will contain `error` key:

```json
{
    "error": "Some error message"
}
```

Find, load and compare the results:

```python
import json

result_json_file = None

for f in task_results['results']:
    if f.endswith('result.json'):
        result_json_file = f
        break

with open(result_json_file, 'r') as f:
    result_json = json.load(f)
assert result_json['data'] == (1 + 2)
```

## Big input files

By default `CreateTask` message cannot exceed 0.5MB. One must use `resources` task's field instead function `args` to supply bigger file inputs. Files listed in `resources` will be laid out in `/golem/resources` directory which is accessible from user supplied function, e.g.:

```python
def echo_task(args):
    my_input = None
    with open('/golem/resources/my_input.txt') as f:
        my_input = f.read()
    return my_input
```

is valid if followed by message:

```python
message = {
    'type': 'CreateTask',
    'task': {
        'type': 'GLambda',
        'options': {
            'method': echo_task,
        },
        'resources': ['my_input.txt']
    }
}
```

## Custom output files

There is no size limit for `result.json` file although one might want to use format different than JSON. To get back results in custom format user has to write them to a file in `/golem/output` directory. Every file in this directory will be packaged and sent back to user if it's listed in `outputs` field of `CreateTask` [message](https://github.com/golemfactory/golemrpc/blob/threaded/docs/messages.md), e.g.: 

```python
def echo_task(args):
    with open('/golem/resources/my_input.txt', 'r') as fin,\
         open('/golem/output/my_output.txt', 'w') as fout:
        fout.write(fin.read())
```

will create `my_output.txt` result file and send it back to user if created by message:

```python
import os
message = {
    'type': 'CreateTask',
    'task': {
        'type': 'GLambda',
        'options': {
            'method': echo_task,
            'outputs': ['my_output.txt']
        },
        'resources': ['{cwd}/my_input.txt'.format(cwd=os.getcwd())]
    }
}
```