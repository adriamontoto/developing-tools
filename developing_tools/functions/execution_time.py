"""
This module contains a decorator that prints the time it took for a function to execute.
"""
from functools import wraps
from time import perf_counter
from typing import Any, Callable


def execution_time(output_decimals: int = 10) -> Callable:
    """
    A decorator that measures and prints the execution time of a function.

    Args:
        output_decimals (int): The number of decimal places to display in the execution time. Defaults to 10.

    Returns:
        Callable: A decorator that wraps a function, measuring its execution time.
    """

    def decorator(function: Callable) -> Callable:
        """
        The actual decorator that wraps the function to measure its execution time.

        Args:
            function (Callable): The function to be decorated.

        Returns:
            Callable: The wrapped function with execution time measurement.
        """

        @wraps(wrapped=function)
        def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            """
            The wrapper function that measures the execution time of the decorated function.

            Args:
                *args: Variable length argument list for the decorated function.
                **kwargs: Arbitrary keyword arguments for the decorated function.

            Returns:
                Any: The result of the decorated function.
            """
            start_time = perf_counter()
            function_output = function(*args, **kwargs)
            execution_time = perf_counter() - start_time

            print(f'Function "{function.__name__}" took {execution_time:.{output_decimals}f} seconds to execute.')

            return function_output

        return wrapper

    return decorator
