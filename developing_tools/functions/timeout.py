"""
Decorator to set a timeout for a function.
"""

from collections.abc import Callable
from functools import wraps
from threading import Thread
from typing import Any


def function_execution(
    function_output: list[Any],
    function: Callable[..., Any],
    args: tuple[Any],
    kwargs: dict[str, Any],
) -> None:
    """
    Execute the function and store the result in the function_output list.

    Args:
        function_output (list[Any]): List to store the function result.
        function (Callable[..., Any]): Function to execute.
        args (tuple[Any]): Function positional arguments.
        kwargs (dict[str, Any]): Function keyword arguments.
    """
    try:
        function_output.append(function(*args, **kwargs))

    except Exception as exception:
        function_output.append(exception)


def timeout(seconds: int | float = 10) -> Callable[..., Any]:
    """
    Decorator to set a timeout for a function.

    Args:
        seconds (int, float, optional): Timeout in seconds. Defaults to 10.

    Raises:
        TypeError: If the timeout seconds is not an integer or a float.
        ValueError: If the timeout seconds is less than or equal to zero.

    Returns:
        Callable[..., Any]: Decorator function.
    """
    if type(seconds) not in [int, float]:
        raise TypeError(f'Timeout seconds must be an integer or a float. Got {type(seconds).__name__}.')

    if seconds <= 0:
        raise ValueError('Timeout seconds must be greater than zero.')

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator to set a timeout for a function.

        Args:
            function (Callable[..., Any]): Function to decorate.

        Returns:
            Callable[..., Any]: Wrapper function.
        """

        @wraps(wrapped=function)
        def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            """
            Wrapper function to execute the decorated function.

            Args:
                *args (tuple[Any]): Positional arguments passed to the decorated function.
                **kwargs (dict[str, Any]): Keyword arguments passed to the decorated function.

            Raises:
                TimeoutError: If the function execution exceeds the timeout.
                Exception: If the decorated function raises an exception.

            Returns:
                Any: The result of the decorated function.
            """
            result: list[Any] = []  # It must be a list to be mutable inside the thread.
            thread = Thread(target=function_execution, args=(result, function, args, kwargs))
            thread.start()

            thread.join(timeout=seconds)
            if thread.is_alive():
                thread.join()
                raise TimeoutError(f'Function {function.__name__} exceeded the {seconds} seconds timeout.')

            if isinstance(result[0], Exception):
                raise result[0]

            return result[0]

        return wrapper

    return decorator
