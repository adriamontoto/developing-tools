"""
This module contains a decorator to enforce compatible and incompatible argument rules on a function.
"""
from functools import wraps
from typing import Any, Callable

from developing_tools.utils.argument_class import Argument


def exclusive_parameters(*arguments: Argument) -> Callable:
    """
    Decorator to enforce compatible and incompatible argument rules on a function.

    Args:
        *arguments (Argument): Variable length Argument objects specifying compatible and incompatible argument rules.

    Returns:
        Callable: The decorated function with argument validation applied.
    """

    def decorator(function: Callable) -> Callable:
        """
        Decorates a function to enforce compatible and incompatible argument rules.

        Args:
            function (Callable): The function to decorate.

        Returns:
            Callable: The wrapped function with argument validation.
        """

        @wraps(wrapped=function)
        def wrapper(*args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
            """
            Wrapper function to enforce argument rules.

            Args:
                *args (tuple[Any]): Positional arguments passed to the decorated function.
                **kwargs (dict[str, Any]): Keyword arguments passed to the decorated function.


            Raises:
                ValueError: If parameters are not accepted by the function.
                ValueError: If incompatible and compatible arguments are used incorrectly.

            Returns:
                Any: The result of the decorated function.
            """
            parameters = set([parameter for sublist in arguments for parameter in sublist.arguments])
            function_parameters = set(function.__annotations__.keys())
            function_parameters.remove('return')

            if parameters - function_parameters:
                raise ValueError(f'Parameters not accepted by function: {parameters - function_parameters}')

            provided_arguments = set(kwargs.keys())
            for argument in arguments:
                compatible_arguments = set(argument.compatible) <= provided_arguments
                incompatible_arguments = set(argument.incompatible) & provided_arguments

                if compatible_arguments and incompatible_arguments:
                    raise ValueError(f'Incompatible arguments used together: {argument.compatible} and {argument.incompatible}')  # yapf: disable

            return function(*args, **kwargs)

        return wrapper

    return decorator
