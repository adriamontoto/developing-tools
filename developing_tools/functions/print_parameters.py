"""
This decorator prints the arguments of a function.
"""

from collections.abc import Callable
from functools import wraps
from typing import Any


def print_parameters(show_types: bool = False, include_return: bool = True) -> Callable[..., Any]:  # noqa: C901
    """
    A decorator that prints the arguments of a function.

    Args:
        show_types (bool, optional): Whether to show the types of the arguments. Defaults to False.
        include_return (bool, optional): Whether to include the return value of the function. Defaults to True.

    Raises:
        TypeError: If the show_types argument is not a boolean.
        TypeError: If the include_return argument is not a boolean.

    Returns:
        Callable[..., Any]: A decorator that wraps a function, printing its arguments.
    """
    if type(show_types) is not bool:
        raise TypeError(f'show_types must be a boolean, got {type(show_types).__name__} instead.')

    if type(include_return) is not bool:
        raise TypeError(f'include_return must be a boolean, got {type(include_return).__name__} instead.')

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
        """
        The actual decorator that wraps the function to print its arguments.

        Args:
            function (Callable[..., Any]): The function to be decorated.

        Returns:
            Callable[..., Any]: The wrapped function with argument printing.
        """

        @wraps(wrapped=function)
        def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            """
            A wrapper function that prints the arguments of the decorated function.

            Args:
                *args (tuple[Any]): Positional arguments passed to the decorated function.
                **kwargs (dict[str, Any]): Keyword arguments passed to the decorated function.

            Returns:
                Any: The result of the decorated function.
            """
            print('Positional arguments:')
            for i, argument in enumerate(args):
                if show_types:
                    print(f'\tArgument {i+1}: value "{argument}", type {type(argument).__name__}')
                else:
                    print(f'\tArgument {i+1}: value "{argument}"')

            print('\nKeyword arguments:')
            for key, value in kwargs.items():
                if show_types:
                    supposed_type = function.__annotations__.get(key, 'Any')
                    supposed_type = supposed_type if supposed_type == 'Any' else supposed_type.__name__

                    print(f'\tArgument {key}: value "{value}", supposed type {supposed_type}, real type {type(value).__name__}')  # fmt: skip  # noqa: E501
                else:
                    print(f'\tArgument {key}: value "{value}"')

            function_output = function(*args, **kwargs)
            if include_return:
                print('\nReturn value:')

                if show_types:
                    supposed_type = function.__annotations__.get('return', 'Any')
                    supposed_type = supposed_type if supposed_type == 'Any' else supposed_type.__name__

                    print(f'\t"{function_output}", supposed type {supposed_type}, real type {type(function_output).__name__}')  # fmt: skip  # noqa: E501
                else:
                    print(f'\t"{function_output}"')

            return function_output

        return wrapper

    return decorator
