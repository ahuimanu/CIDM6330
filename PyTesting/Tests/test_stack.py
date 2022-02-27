import pytest
from DataStructures.stack import Stack

# pytest fixtures help with the arrange portion of testing

@pytest.fixture
def t_stack():
    return Stack()

# we are injecting the fixture here
def test_can_create_stack(t_stack):
    # arrange
    # act

    # https://docs.python.org/3.8/library/functions.html#isinstance
    # assert
    assert isinstance(t_stack, Stack)
    assert len(t_stack) == 0

# we are injecting the fixture here
def test_can_push_to_stack(t_stack):
    t_stack.push(3)
    assert len(t_stack) == 1

def test_can_pop_from_stack(t_stack):
    pushed_item = "test item"
    t_stack.push("test item")
    assert t_stack.pop() == pushed_item
    assert t_stack.pop() is None