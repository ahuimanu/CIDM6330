import pytest
from avform.conversions import ( 
    knots_to_kph,
    knots_to_fps,
    knots_to_mph,
    mph_to_knots,
    mph_to_kph,
    mph_to_fps,
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

def test_mph_to_knots():
    mph = 3
    knots = mph_to_knots(mph)
    assert knots == 2.606928

def test_mph_to_kph():
    mph = 3
    kph = mph_to_kph(mph)
    assert kph == 4.828032

def test_mph_to_fps():
    mph = 3
    fps = mph_to_fps(3)
    assert fps == 4.400001



# def kph_to_knots(kph: float) -> float:
#     return kph * 0.539968

# def kph_to_fps(kph: float) -> float:
#     return kph * 0.911344

# def kph_to_mph(kph: float) -> float:
#     return kph * 0.621371    