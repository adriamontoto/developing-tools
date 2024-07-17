"""
This module contains the Argument class, which represents an argument with conditions on how it can be combined with
other arguments.
"""


class Argument:
    """
    Represents an argument with conditions on how it can be combined with other arguments.
    """

    __compatible: list[str]
    __incompatible: list[str]

    def __init__(self, compatible: list[str], incompatible: list[str]) -> None:
        """
        Initializes the Argument object with optional compatible and incompatible lists.

        Args:
            compatible (list[str]): A list of argument names that can be used together.
            incompatible (list[str]): A list of argument names that cannot be used with the 'compatible' arguments.
        """
        self.__compatible = compatible or []
        self.__incompatible = incompatible or []

    @property
    def arguments(self) -> list[str]:
        """
        Returns the combined list of 'compatible' and 'incompatible' arguments, ensuring uniqueness.

        Returns:
            list[str]: The unique list of parameters.
        """
        return list(set(self.__compatible + self.__incompatible))

    @property
    def compatible(self) -> list[str]:
        """
        Returns the list of arguments that can be used together.

        Returns:
            list[str]: The list of 'compatible' arguments.
        """
        return self.__compatible

    @property
    def incompatible(self) -> list[str]:
        """
        Returns the list of arguments that cannot be used with the 'compatible' arguments.

        Returns:
            list[str]: The list of 'incompatible' arguments.
        """
        return self.__incompatible
