import pytest

from dectorom import number_to_numeral

def test_number_to_number_func():

    #arrange
    #act
    #assert
    assert number_to_numeral(123) == "CXXIII"
    assert number_to_numeral(2023) == "MMXXIIII"