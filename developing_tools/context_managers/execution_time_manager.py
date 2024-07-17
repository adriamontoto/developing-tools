"""
A context manager for measuring the execution time of code blocks.
"""

from time import perf_counter
from types import NoneType, TracebackType
from typing import Self


class ExecutionTimeBlock:
    """
    A context manager for measuring the execution time of code blocks.
    """

    __title: str | None
    __output_decimals: int
    __start_time: float
    __end_time: float
    __execution_time: float

    def __init__(self, title: str | None = None, output_decimals: int = 10) -> None:
        """
        Initializes the ExecutionTimeBlock context manager.

        Args:
            title (str | None, optional): Title for the code block being timed. Defaults to None.
            output_decimals (int, optional): Number of decimal places to include in the printed execution time. Defaults
            to 10.

        Raises:
            TypeError: If the title argument is not a string or None.
            TypeError: If the output_decimals argument is not an integer.
            ValueError: If the output_decimals argument is a negative integer.
        """
        if type(title) not in [str, NoneType]:
            raise TypeError(f'Title must be a string, got {type(title).__name__} instead.')

        if type(output_decimals) is not int:
            raise TypeError(f'output_decimals must be an integer, got {type(output_decimals).__name__} instead.')

        if output_decimals < 0:
            raise ValueError(f'output_decimals must be a non-negative integer, got {output_decimals} instead.')

        self.__title = title
        self.__output_decimals = output_decimals

    def __enter__(self) -> Self:
        """
        Automatically called at the beginning of the block after the 'with' statement, and starts the
        ExecutionTimeBlock.

        Returns:
            Self: Returns itself to be used in the 'with' statement.
        """
        self.__start_time = perf_counter()
        return self

    def __exit__(self, exc_type: type | None, exc_val: Exception | None, exc_tb: TracebackType | None) -> None:
        """
        Exit the runtime context related to this object, additionally printing the execution time of the code wrapped
        in the with statement.

        Args:
            exc_type (type | None): The type of the exception that caused the context to be exited. None if the context
            was exited without an exception.
            exc_val (Exception | None): The exception that caused the context to be exited. None if the context was
            exited without an exception.
            exc_tb (TracebackType | None): The traceback object for the exception. None if the context was exited
            without an exception.
        """
        self.__end_time = perf_counter()
        self.__execution_time = self.__end_time - self.__start_time

        if self.__title is None:
            print(f'This code took {self.execution_time:.{self.output_decimals}f} seconds to execute.')
        else:
            print(f'Code block with title "{self.title}" took {self.execution_time:.{self.output_decimals}f} seconds to execute.')  # fmt: skip  # noqa: E501

    @property
    def title(self) -> str | None:
        """
        Returns the title for the code block being timed.

        Returns:
            str | None: The title for the code block being timed.
        """
        return self.__title

    @property
    def output_decimals(self) -> int:
        """
        Returns the number of decimal places to include in the printed execution time.

        Returns:
            int: The number of decimal places to include in the printed execution time.
        """
        return self.__output_decimals

    @property
    def start_time(self) -> float:
        """
        Returns the start time of the ExecutionTimeBlock.

        Returns:
            float: The start time of the ExecutionTimeBlock.
        """
        return self.__start_time

    @property
    def end_time(self) -> float:
        """
        Returns the end time of the ExecutionTimeBlock.

        Returns:
            float: The end time of the ExecutionTimeBlock.
        """
        return self.__end_time

    @property
    def execution_time(self) -> float:
        """
        Returns the execution time of the code wrapped in the with statement.

        Returns:
            float: The execution time of the code wrapped in the with statement.
        """
        return self.__execution_time
