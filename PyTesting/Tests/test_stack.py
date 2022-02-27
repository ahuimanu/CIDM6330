from DataStructures.stack import Stack


def test_can_create_stack():
    # arrange
    # act
    s = Stack()

    # https://docs.python.org/3.8/library/functions.html#isinstance
    # assert
    assert isinstance(s, Stack)
    assert len(s) == 0
