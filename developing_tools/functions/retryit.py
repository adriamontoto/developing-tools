"""
This module contains a decorator that retries to execute a function a given number of times.
"""

from collections.abc import Callable
from functools import wraps
from random import SystemRandom
from time import sleep
from typing import Any


def retryit(  # noqa: C901
    attempts: int | None = None,
    delay: float | tuple[float, float] = 5,
    raise_exception: bool = True,
    valid_exceptions: tuple[type[Exception]] | None = None,
) -> Callable[..., Any]:
    """
    Decorator that retries to execute a function a given number of times.

    Args:
        attempts (int, optional): The number of attempts to execute the function, if None the function will be executed
        indefinitely until it succeeds or the program is interrupted. Default is None.
        delay (float | tuple[float, float], optional): The number of seconds to wait before each attempt, if a tuple is
        provided, a random delay between the two values will be used (both included). Default is 5 seconds.
        raise_exception (bool, optional): Whether to raise an exception if the function fails after all attempts.
        Default is True.
        valid_exceptions (tuple[type[Exception]], optional): A tuple of exceptions that should be caught and
        retried. If None, all exceptions will be caught. Default is None. Exception subclasses are also caught.

    Raises:
        TypeError: If the number of attempts is not an integer.
        ValueError: If the number of attempts is less than 1.
        TypeError: If the delay is not a number or a tuple.
        ValueError: If the delay is less than 0.
        TypeError: If the delay tuple has elements that are not numbers.
        ValueError: If the delay tuple does not have 2 elements.
        ValueError: If the delay tuple has elements that are less than 0.
        ValueError: If the first element of the delay tuple is greater than or equal to the second element.
        TypeError: If raise_exception is not a boolean.
        TypeError: If valid_exceptions is not a tuple.
        ValueError: If valid_exceptions is empty.
        TypeError: If the elements of valid_exceptions are not exception types.

    Returns:
        Callable[..., Any]: The decorated function.
    """
    if attempts is not None:
        if type(attempts) is not int:
            raise TypeError(f'The number of attempts must be an integer. Got {type(attempts).__name__} instead.')

        if attempts < 1:
            raise ValueError(f'The number of attempts must be greater than 0. Got {attempts} instead.')

    if type(delay) not in [int, float, tuple]:
        raise TypeError(f'The delay must be a number or a tuple. Got {type(delay).__name__} instead.')

    if type(delay) in [int, float] and delay < 0:  # type: ignore
        raise ValueError(f'The delay must be greater than or equal to 0. Got {delay} instead.')

    if type(delay) is tuple:
        if len(delay) != 2:
            raise ValueError(f'The delay tuple must have 2 elements. Got {len(delay)} instead.')

        for element in delay:
            if type(element) not in [int, float]:
                raise TypeError(f'Both elements of the delay tuple must be numbers. Got {type(element).__name__} instead.')  # fmt: skip  # noqa: E501

        if delay[0] < 0 or delay[1] < 0:
            raise ValueError(f'Both elements of the delay tuple must be greater than or equal to 0. Got {delay} instead.')  # fmt: skip  # noqa: E501

        if delay[0] >= delay[1]:
            raise ValueError(f'The first element of the delay tuple must be less than to the second element. Got {delay} instead.')  # fmt: skip  # noqa: E501

    if type(raise_exception) is not bool:
        raise TypeError(f'raise_exception must be a boolean. Got {type(raise_exception).__name__} instead.')

    if valid_exceptions is not None:
        if not isinstance(valid_exceptions, tuple):
            raise TypeError(f'valid_exceptions must be a tuple. Got {type(valid_exceptions).__name__} instead.')

        if not len(valid_exceptions):
            raise ValueError('valid_exceptions must have at least one element.')

        for exception in valid_exceptions:
            if not isinstance(exception, type) or not issubclass(exception, Exception):  # type: ignore
                raise TypeError(f'All elements of valid_exceptions must be exception types. Got {type(exception).__name__} instead.')  # fmt: skip  # noqa: E501

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator that retries to execute a function a given number of times.

        Args:
            function (Callable[..., Any]): The function to decorate.

        Returns:
            Callable[..., Any]: The decorated function.
        """

        @wraps(wrapped=function)
        def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            """
            Wrapper function that retries to execute a function a given number of times.

            Args:
                *args (tuple[Any]): Positional arguments passed to the decorated function.
                **kwargs (dict[str, Any]): Keyword arguments passed to the decorated function.

            Returns:
                Any: The result of the decorated function.
            """
            attempt = 0
            _delay = delay
            while attempts is None or attempts > 0:
                if type(delay) is tuple:
                    _delay = SystemRandom().uniform(a=delay[0], b=delay[1])

                if attempts:
                    print(f'Attempt [{attempt + 1}/{attempts}] to execute function "{function.__name__}".')
                else:
                    print(f'Attempt {attempt + 1} to execute function "{function.__name__}".')

                try:
                    return function(*args, **kwargs)

                except valid_exceptions or Exception as exception:  # noqa: B030
                    error_message = str(exception).rstrip('.')

                    if (attempt + 1) == attempts:
                        print(f'Function failed with error: "{error_message}". No more attempts.')
                        if raise_exception:
                            raise exception

                        return

                    print(f'Function failed with error: "{error_message}". Retrying in {_delay:.2f} seconds ...')
                    sleep(_delay)  # type: ignore
                    attempt += 1

            return

        return wrapper

    return decorator
