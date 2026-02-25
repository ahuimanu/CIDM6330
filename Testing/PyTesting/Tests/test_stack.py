import pytest
from DataStructures.stack import Stack


@pytest.fixture
def t_stack():
    return Stack()


def test_can_create_stack(t_stack):
    # arrange
    # act
    # https://docs.python.org/3.8/library/functions.html#isinstance
    # assert
    assert isinstance(t_stack, Stack)
    assert len(t_stack) == 0


def test_can_push_to_stack(t_stack):
    t_stack.push(99)
    assert len(t_stack) == 1


def test_can_pop_from_stack(t_stack):
    pushed_item = "test item"
    t_stack.push(pushed_item)
    assert t_stack.pop() == pushed_item
    assert t_stack.pop() is None
