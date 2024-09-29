<a name="readme-top"></a>

# 🐣💻 Developing Tools
<p align="center">
    <a href="https://github.com/adriamontoto/developing-tools/actions/workflows/test.yaml?event=push&branch=master" target="_blank">
        <img src="https://github.com/adriamontoto/developing-tools/actions/workflows/test.yaml/badge.svg?event=push&branch=master" alt="Test Pipeline">
    </a>
    <a href="https://github.com/adriamontoto/developing-tools/actions/workflows/lint.yaml?event=push&branch=master" target="_blank">
        <img src="https://github.com/adriamontoto/developing-tools/actions/workflows/lint.yaml/badge.svg?event=push&branch=master" alt="Lint Pipeline">
    </a>
        <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/adriamontoto/developing-tools" target="_blank">
        <img src="https://coverage-badge.samuelcolvin.workers.dev/adriamontoto/developing-tools.svg" alt="Coverage Pipeline">
    </a>
    <a href="https://pypi.org/project/developing-tools" target="_blank">
        <img src="https://img.shields.io/pypi/v/developing-tools?color=%2334D058&label=pypi%20package" alt="Package Version">
    </a>
    <a href="https://pypi.org/project/developing-tools/" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/developing-tools.svg?color=%2334D058" alt="Supported Python Versions">
    </a>
</p>

The "Developing Tools" project is a Python 🐍 package designed to enhance the development process by providing a collection of tools/utilities aimed at improving debugging, performance measurement, error handling, ...

These tools ⚒️ are intended to assist developers in identifying performance bottlenecks, handling transient errors, and gaining insights into function behavior during runtime. The package is easy to install and use, making it a good addition to any Python developer's toolkit 🚀.
<br><br>


## Table of Contents
- [📥 Installation](#installation)
- [💻 Utilization](#utilization)
- [🔑 License](#license)
<br><br>

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>



<a name="installation"></a>
## 📥 Installation
```bash
pip install developing-tools
```
<br><br>

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>



<a name="utilization"></a>
## 💻 Utilization
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

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

### Retry It
The `retryit` decorator allows you to retry a function multiple times in case of failure. The decorator has two parameters:

- `attempts`: The number of attempts to execute the function, if _None_ the function will be executed indefinitely. Default is _None_.
- `delay`: The delay between attempts in seconds, if a tuple is provided the delay will be randomized between the two values. Default is 5 seconds.
- `raise_exception`: If _True_ the decorator will raise the last caught exception if the function fails all attempts. Default is _True_.
- `valid_exceptions`: A tuple of exceptions that the decorator should catch and retry the function, if _None_ the decorator will catch all exceptions. Default is _None_.

```python
from developing_tools.functions import retryit

@retryit(attempts=3, delay=0.5, raise_exception=True, valid_exceptions=(ValueError,))
def failing_function() -> None:
    raise ValueError('This function always fails!')

failing_function()

# >>> Function failed with error: "This function always fails!". Retrying in 0.50 seconds ...
# >>> Attempt [2/3] to execute function "failing_function".
# >>> Function failed with error: "This function always fails!". Retrying in 0.50 seconds ...
# >>> Attempt [3/3] to execute function "failing_function".
# >>> Function failed with error: "This function always fails!". No more attempts.
# Traceback (most recent call last):
#   File "<file_path>/main.py", line 7, in <module>
#     failing_function()
#   File "<file_path>/developing_tools/functions/retryit.py", line 132, in wrapper
#     raise exception
#   File "<file_path>/developing_tools/functions/retryit.py", line 124, in wrapper
#     return function(*args, **kwargs)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "<file_path>/main.py", line 5, in failing_function
#     raise ValueError('This function always fails!')
# ValueError: This function always fails!
```
<br>

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>


### Print Parameters
The `print_parameters` decorator allows you to print the parameters of a function. The decorator has two parameters:

- `show_types`: If _True_ the decorator will print the types of the parameters. Default is _False_.
- `include_return`: If _True_ the decorator will print the return value of the function. Default is _True_.

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
<br>

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>

### Timeout
The `timeout` decorator allows you to set a maximum execution time for a function. The decorator has one parameter:

- `seconds`: The maximum number of seconds the function is allowed to execute before raising a _TimeoutError_. Default is 10 seconds.

```python
from time import sleep
from developing_tools.functions import timeout

@timeout(seconds=2)
def too_slow_function() -> None:
    sleep(5)

too_slow_function()

# >>> TimeoutError: Function too_slow_function exceeded the 2 seconds timeout.
```
<br><br>

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>


<a name="license"></a>
## 🔑 License
This project is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/mit/).
<br><br>

<p align="right">
    <a href="#readme-top">🔼 Back to top</a>
</p>
