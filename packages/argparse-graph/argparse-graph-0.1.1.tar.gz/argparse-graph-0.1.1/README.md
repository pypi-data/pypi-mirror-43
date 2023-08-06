# agrparseGraph

## Summary

- [Description](#description)
- [Install](#install)
- [Use it](#user-it)
- [Tests](#test)
- [Documentation](#documentation)

## Description
Add logic in argpars object with argparsGraph.  
This package helps you to avoid the if/else forestswhen using `argparse`

## Install

Install package:
```shell
pip install argparse-graph
```

Uninstall package:
```shell
pip uninstall argparse-graph
```

**manually :**

Install the package:
```shell
make install
```

Uninstall the package:
```shell
make uninstall
```

## Use it

> The parameter defined with argparse must be named (dest="argsName")if not, it will  
> be impossible to find some link between the variable name and the name in the yaml file.

example of argparse object:

**python script**
```python
from argparseGraph.argparseGraph import argparseGraph as agg

def parsarg():
    parser = argparse.ArgumentParser(description="random options for differents cenarios")
    parser.add_argument("-q", dest="argv1", help="test", type=int)
    parser.add_argument("-w", dest="argv2", help="test", type=int, action='append')
    parser.add_argument("-e", dest="argv3", help="test", type=str, default="test3")
    parser.add_argument("-t", dest="argv4", help="test", type=str, default=False)
    parser.add_argument("-a", dest="argv5", help="test", type=str)
    parser.add_argument("-s", dest="argv6", help="test", type=bool)
    parser.add_argument("-d", dest="argv7", help="test", type=str, action='append')
    args = parser.parse_args()

    return args

res = parsarg()
agg = agg("scenarios.yml", res_args, verbose=False)
```

**scenario.yml**
```yaml
# if all parameters are not None
# cmd: ./main.py -q 1 -w 1 -w 2 -e t -t o -a o -s t -d "Hello"  -d "World"
scenario_1:
  options: "all"
# if argv3, argv4 are not None and other are None
# format list [v1, v2]
# cmd: ./main.py -e toto -t ok
scenario_2:
  options: [argv3, argv4]
# if argv3, argv4, argv5, argv6, argv7 are not None and other are None
# format list     
#    - argv3
#    - argv4
#    - argv5
#    - argv6
#    - argv7
# cmd: ./main.py -e toto -t ok -a ok -s True -d "Hello"  -d "World"
scenario_3:
  options:
    - argv3
    - argv4
    - argv5
    - argv6
    - argv7
# if argv3, argv4, argv6, argv7 are not None and other are None
# format str argv3, argv4, argv6, argv7
# cmd: ./main.py -s False -t True -d "Test"
scenario_4:
  options: argv3, argv4, argv6, argv7
```

With the `argparseGraph` object you can get 3 differents results formats,
with those methods:  
```python
# Return the name of the strategie in the yaml file.
agg.get_one()
# example:
# 'scenario_test'

# Return a dict
agg.get_dict()
# { 'scenario': 'scenario_test', 'options': ['argv3', 'argv4', 'argv5', 'argv6', 'argv7'], 'status': None}

agg.get_all()
# {
#  'scenario_1': {'options': 'all', 'name': 'scenario_1', 'status': 'Fail'},
#  'scenario_2': {'options': ['argv3', 'argv4'], 'name': 'scenario_2', 'status': 'Fail'},
#  'scenario_3': {'options': ['argv3', 'argv4'], 'name': 'scenario_3', 'status': 'Fail'},
#  'scenario_4': {'options': ['argv3', 'argv4', 'argv6', 'argv7'], 'name': 'scenario_4', 'status': 'Fail'},
#  'scenario_test': {'options': ['argv3', 'argv4', 'argv5', 'argv6', 'argv7'], 'name': 'scenario_test', 'status': None},
#  'scenario_5': {'options': '', 'name': 'scenario_5', 'status': 'Fail'}
# }
```

## Tests

Two types of tests are available, the first one is running on the sources in the project directory,
the second one is running on the package install on your system.

run test on the package not installed:
```
make test
```

run test on the package installed:
```
make test_install
```


## Documentation

_Makefile commands available_:

|          **Commands name**           | **Description**                       |
|:------------------------------------:|:------------------------------------- |
|            `make install`            | install `argparseGraph`               |
|                                      |                                       |
|           `make uninstall`           | uninstall `argparseGraph`             |
|                                      |                                       |
|             `make test`              | run test on sources not installed     |
|                                      |                                       |
|         `make test_install`          | run test on the package installed     |
|                                      |                                       |
|              `make run`              | run example                           |
| `make run scenarios=[1 , 2, 3, 4, 5]` | run example with a specifique scenarios|
|                                      |                                       |

you can specify makefile options:

|    **Define name**    | **Default** | **Description**                             |
|:---------------------:|:----------- | ------------------------------------------- |
|  `EXEC_DEFAULT_TEST`  | pytest      | Tools to run tests                          |
|                       |             |                                             |
| `PYTHON_DEFAULT_EXEC` | python3     | Use Python to run tests and install package |
|                       |             |                                             |


**Credit Idea Gael Rottier**
  - [Medium](https://medium.com/@gaelrottier)
  - [Linkedin](https://www.linkedin.com/in/gaël-rottier-53080263/)

__Reference__:

- [Python3.5 Documentation](https://www.python.org/downloads/release/python-350/)
- [argparse (python3)](https://docs.python.org/3/library/argparse.html)
- [pip](https://pip.pypa.io/en/stable/)
- [setuptools](https://setuptools.readthedocs.io/en/latest/)
