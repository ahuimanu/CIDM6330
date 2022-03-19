"""
https://edwilliams.org/avform147.htm#Conv
 
 1 knot = 1.852000 km/hr*
 1 knot = 185200/109728 ft/sec* =1.687810 ft/sec
 1 knot = 1852000/1609344 mph* = 1.150779 mph
 1 mph  = 0.868976 knot
 1 mph  = 1.609344 km/hr*
 1 mph  = 1.466667 ft/sec
 1 km/hr= 0.539968 knot
 1 km/hr= 0.911344 ft/sec
 1 km/hr= 0.621371 mph
"""


def knots_to_kph(knots: float) -> float:
    return knots * 1.852000


def knots_to_fps(knots: float) -> float:
    return knots * 1.687810


def knots_to_mph(knots: float) -> float:
    return knots * 1.150779


def mph_to_knots(mph: float) -> float:
    return mph * 0.868976


def mph_to_kph(mph: float) -> float:
    return mph * 1.609344


def mph_to_fps(mph: float) -> float:
    return mph * 1.466667


def kph_to_knots(kph: float) -> float:
    return kph * 0.539968


def kph_to_fps(kph: float) -> float:
    return kph * 0.911344


def kph_to_mph(kph: float) -> float:
    return kph * 0.621371
