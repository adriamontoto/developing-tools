"""
Singleton Pattern metaclass to be used in the creation of singletons.
"""

from threading import Lock
from typing import Any, ClassVar
from typing_extensions import override


class SingletonPattern(type):
    """
    Singleton Pattern metaclass to be used in the creation of singletons (thread-safe).
    """

    __instances: ClassVar = {}
    __lock: Lock = Lock()

    @override
    def __call__(cls, *args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        """
        Returns the singleton instance of the class. If the instance does not exist, it creates a new one using the
        provided arguments. Subsequent calls to this method will return the previously created instance,
        ignoring any arguments provided.

        Args:
            *args (tuple[Any]): Positional arguments to be used in the creation of the singleton instance.
            **kwargs (dict[str, Any]): Keyword arguments to be used in the creation of the singleton instance.

        Returns:
            Any: The singleton instance of the class.
        """
        with cls.__lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super().__call__(*args, **kwargs)

        return cls.__instances[cls]
