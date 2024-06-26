# 🐣💻 Developing Tools
The "Developing Tools" project is a Python 🐍 package designed to enhance the development process by providing a collection of tools/utilities aimed at improving debugging, performance measurement, error handling, ...

These tools ⚒️ are intended to assist developers in identifying performance bottlenecks, handling transient errors, and gaining insights into function behavior during runtime. The package is easy to install and use, making it a good addition to any Python developer's toolkit 🚀.
<br><br>


## Table of Contents
- [Installation](#installation)
- [Utilization](#utilization)
- [License](#license)
<br><br>


## Installation
```bash
pip install developing-tools
```
<br><br>


## Utilization
### Execution Time
The `execution_time` decorator allows you to measure the execution time of a function. The decorator has one parameter:
- `output_decimals`: Number of decimal places to display in the output. Default is 10.

```python
from time import sleep
from developing_tools.functions import execution_time

@execution_time(output_decimals=2)
def too_slow_function() -> None:
    sleep(2)

too_slow_function()

# >>> Function "too_slow_function" took 2.00 seconds to execute.
```
<br>

### Retry It
The `retryit` decorator allows you to retry a function multiple times in case of failure. The decorator has two parameters:
- `attempts`: The number of attempts to execute the function, if *None* the function will be executed indefinitely. Default is *None*.
- `delay`: The delay between attempts in seconds, if a tuple is provided the delay will be randomized between the two values. Default is 5 seconds.

```python
from developing_tools.functions import retryit

@retryit(attempts=3, delay=0.5)
def failing_function() -> None:
    raise ValueError('This function always fails!')

failing_function()

# >>> Function failed with error: "This function always fails!". Retrying in 0.50 seconds ...
# >>> Attempt [2/3] to execute function "failing_function".
# >>> Function failed with error: "This function always fails!". Retrying in 0.50 seconds ...
# >>> Attempt [3/3] to execute function "failing_function".
# >>> Function failed with error: "This function always fails!". No more attempts.
```
<br>

### Print Parameters
The `print_parameters` decorator allows you to print the parameters of a function. The decorator has two parameters:
- `show_types`: If *True* the decorator will print the types of the parameters. Default is *False*.
- `include_return`: If *True* the decorator will print the return value of the function. Default is *True*.

```python
from developing_tools.functions import print_parameters

@print_parameters(show_types=True, include_return=True)
def normal_function(a: int, b: str, c: int, d) -> str:
    return a

normal_function(1, 'Hello', c=3, d=4)

# >>> Positional arguments:
# >>>         Argument 1: value "1", type int
# >>>         Argument 2: value "Hello", type str
# >>>
# >>> Keyword arguments:
# >>>         Argument c: value "3", supposed type int, real type int
# >>>         Argument d: value "4", supposed type Any, real type int
# >>>
# >>> Return value:
# >>>         "1", supposed type str, real type int
```
<br><br>


## License
This project is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/mit/).
