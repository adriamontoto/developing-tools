"""
Test ExecutionTimeBlock context manager.
"""

from datetime import UTC, datetime

from freezegun import freeze_time
from pytest import CaptureFixture, mark, raises as pytest_raises

from developing_tools.context_managers import ExecutionTimeBlock


@mark.parametrize('title, output_decimals', [(None, 5), ('Test Block', 3), (None, 0), ('Test Block', 10)])
def test_execution_time_manager(title: str | None, output_decimals: int) -> None:
    """
    Test that the ExecutionTimeBlock context manager can be used to time a code block.

    Args:
        title (str | None): Title for the code block being timed.
        output_decimals (int): Number of decimal places to include in the printed execution time.
    """
    with freeze_time(time_to_freeze='2021-01-01') as frozen_time:  # noqa: SIM117
        with ExecutionTimeBlock(title=title, output_decimals=output_decimals) as context:
            frozen_time.tick(delta=60)

    assert context.title == title
    assert context.output_decimals == output_decimals
    assert context.start_time == datetime(year=2021, month=1, day=1, tzinfo=UTC).timestamp()
    assert context.end_time == datetime(year=2021, month=1, day=1, tzinfo=UTC).timestamp() + 60
    assert context.execution_time == 60


@freeze_time(time_to_freeze='2021-01-01')
def test_execution_time_manager_start_time() -> None:
    """
    Test that the start_time property of the ExecutionTimeBlock context manager is set to the current time when the
    block is entered.
    """
    with ExecutionTimeBlock() as context:
        assert context.start_time == datetime(year=2021, month=1, day=1, tzinfo=UTC).timestamp()


@freeze_time(time_to_freeze='2021-01-01')
def test_execution_time_manager_end_time() -> None:
    """
    Test that the end_time property of the ExecutionTimeBlock context manager is set to the current time when the block
    is exited.
    """
    with ExecutionTimeBlock() as context:
        pass

    assert context.end_time == datetime(year=2021, month=1, day=1, tzinfo=UTC).timestamp()


def test_execution_time_manager_execution_time() -> None:
    """
    Test that the execution_time property of the ExecutionTimeBlock context manager is set to the difference between the
    end_time and start_time properties.
    """
    with ExecutionTimeBlock() as context:
        pass

    assert context.execution_time == context.end_time - context.start_time


@freeze_time(time_to_freeze='2021-01-01')
@mark.parametrize('title, output_decimals', [(None, 5), ('Test Block', 3), (None, 0), ('Test Block', 10)])
def test_execution_time_manager_output(capsys: CaptureFixture[str], title: str | None, output_decimals: int) -> None:
    """
    Test that the ExecutionTimeBlock context manager prints the execution time of the code block with the correct title
    and number of decimal places.

    Args:
        capsys (CaptureFixture[str]): Pytest fixture to capture stdout and stderr.
        title (str | None): Title for the code block being timed.
        output_decimals (int): Number of decimal places to include in the printed execution time.
    """
    with ExecutionTimeBlock(title=title, output_decimals=output_decimals) as context:
        pass

    if title is None:
        message = f'This code took {context.execution_time:.{output_decimals}f} seconds to execute.\n'
    else:
        message = f'Code block with title "{title}" took {context.execution_time:.{output_decimals}f} seconds to execute.\n'  # fmt: skip  # noqa: E501

    out, _ = capsys.readouterr()
    assert out == message


@mark.parametrize('title', [123, 3.14, True, [], {}])
def test_execution_time_manager_invalid_title_type(title: str) -> None:
    """
    Test that the ExecutionTimeBlock context manager raises a TypeError when the title argument is not a string or None.

    Args:
        title (str): Title for the code block being timed.
    """
    with pytest_raises(
        expected_exception=TypeError,
        match=f'Title must be a string, got {type(title).__name__} instead.',
    ):
        ExecutionTimeBlock(title=title)


def test_execution_time_manager_title_can_not_be_changed() -> None:
    """
    Test that the title property of the ExecutionTimeBlock context manager can not be changed after initialization.
    """
    context = ExecutionTimeBlock(title='Test Block', output_decimals=5)

    with pytest_raises(expected_exception=AttributeError):
        context.title = 'New Title'  # type: ignore


@mark.parametrize('output_decimals', ['five', 3.14, True, [], {}, None])
def test_execution_time_manager_invalid_output_decimals_type(output_decimals: int) -> None:
    """
    Test that the ExecutionTimeBlock context manager raises a TypeError when the output_decimals argument is not an
    integer.

    Args:
        output_decimals (int): Number of decimal places to include in the printed execution time.
    """
    with pytest_raises(
        expected_exception=TypeError,
        match=f'output_decimals must be an integer, got {type(output_decimals).__name__} instead.',
    ):
        ExecutionTimeBlock(output_decimals=output_decimals)


@mark.parametrize('output_decimals', [-100, -5, -1])
def test_execution_time_manager_invalid_output_decimals_value(output_decimals: int) -> None:
    """
    Test that the ExecutionTimeBlock context manager raises a ValueError when the output_decimals argument is a negative
    integer.

    Args:
        output_decimals (int): Number of decimal places to include in the printed execution time.
    """
    with pytest_raises(
        expected_exception=ValueError,
        match=f'output_decimals must be a non-negative integer, got {output_decimals} instead.',
    ):
        ExecutionTimeBlock(output_decimals=output_decimals)


def test_execution_time_manager_output_decimals_can_not_be_changed() -> None:
    """
    Test that the output_decimals property of the ExecutionTimeBlock context manager can not be changed after
    initialization.
    """
    context = ExecutionTimeBlock(title='Test Block', output_decimals=5)

    with pytest_raises(expected_exception=AttributeError):
        context.output_decimals = 3  # type: ignore


def test_execution_time_manager_start_time_can_not_be_changed() -> None:
    """
    Test that the start_time property of the ExecutionTimeBlock context manager can not be changed after initialization.
    """
    context = ExecutionTimeBlock(title='Test Block', output_decimals=5)

    with pytest_raises(expected_exception=AttributeError):
        context.start_time = 3.5  # type: ignore


def test_execution_time_manager_end_time_can_not_be_changed() -> None:
    """
    Test that the end_time property of the ExecutionTimeBlock context manager can not be changed after initialization.
    """
    context = ExecutionTimeBlock(title='Test Block', output_decimals=5)

    with pytest_raises(expected_exception=AttributeError):
        context.end_time = 3.5  # type: ignore


def test_execution_time_manager_execution_time_can_not_be_changed() -> None:
    """
    Test that the execution_time property of the ExecutionTimeBlock context manager can not be changed after
    initialization.
    """
    context = ExecutionTimeBlock(title='Test Block', output_decimals=5)

    with pytest_raises(expected_exception=AttributeError):
        context.execution_time = 3.5  # type: ignore
