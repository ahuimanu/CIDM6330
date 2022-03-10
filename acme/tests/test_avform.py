import pytest
from avform.conversions import ( 
    knots_to_kph,
    knots_to_fps,
    knots_to_mph,
)

def test_knots_to_kph():
    knots = 3
    kph = knots_to_kph(knots)
    assert kph == 5.556

def test_knots_to_fps():
    knots = 3
    fps = knots_to_fps(knots)
    assert fps == 5.06343 

def test_knots_to_mph():
    knots = 3
    mph = knots_to_mph(knots)
    assert mph == 3.452337