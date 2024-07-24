"""
Test the singleton pattern.
"""

from threading import Thread

from developing_tools.patterns import SingletonPattern


class TestSingletonClass(metaclass=SingletonPattern):
    """
    Test class for the singleton pattern.
    """

    pass


def test_singleton_instance() -> None:
    """
    Test that the singleton pattern returns the same instance.
    """
    instance1 = TestSingletonClass()
    instance2 = TestSingletonClass()

    assert instance1 is instance2


def test_singleton_thread_safety() -> None:
    """
    Test that the singleton pattern is thread-safe.
    """

    def create_instance(results: dict[int, TestSingletonClass], index: int) -> None:
        """
        Create an instance of the singleton class.

        Args:
            results (dict): The dictionary to store the results.
            index (int): The index of the instance.
        """
        results[index] = TestSingletonClass()

    results: dict[int, TestSingletonClass] = {}

    thread1 = Thread(target=create_instance, args=(results, 1))
    thread2 = Thread(target=create_instance, args=(results, 2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert results[1] is results[2]
