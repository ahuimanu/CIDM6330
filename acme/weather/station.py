import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from enum import Enum, IntEnum


class StationType(IntEnum):
    """
    https://aviationweather.gov/dataserver/fields?datatype=station
    The station type, which can be a combination of the following:
    METAR | rawinsonde | TAF | NEXRAD | wind_profiler | WFO_office | SYNOPS

    Useful information on enums: https://betterprogramming.pub/enumerations-in-python-b01a1fb479de
    """

    METAR = 0
    rawinsonde = 1
    TAF = 2
    NEXRAD = 3
    wind_profiler = 4
    WFO_office = 5
    SYNOPS = 6


@dataclass
class Station:
    """
    https://aviationweather.gov/dataserver/fields?datatype=station

    """

    station_id: str = ""  # The 4-letter station specifier
    wmo_id: str = ""  # Four-letter WMO Id for the station
    latitude: float = 0.0  # The latitude in decimal degrees
    longitude: float = 0.0  # The longitude in decimal degrees
    elevation_m: float = (
        0.0  # The elevation of the station in MSL (above mean sea-level)
    )
    site: str = ""  # The "common" name/human-readable name of the station
    state: str = (
        ""  # The two-letter abbreviation for the U.S. state or Canadian province
    )
    country: str = ""  # The two-letter country abbreviation
    site_type: StationType = StationType.METAR

    # properties - https://docs.python.org/3/library/functions.html#property


class StationHelper(ABC):
    """
    A utility class containing routines to assist in creating stations
    """

    # static methods - https://docs.python.org/3/library/functions.html#staticmethod
    # abstract methods - https://docs.python.org/3/library/abc.html#abc.abstractmethod
    @staticmethod
    @abstractmethod
    def get_station_from_station_id(station_id: str) -> Station:
        pass

    @staticmethod
    @abstractmethod
    def get_station_from_lat_lon(latitude: float, longitude: float) -> Station:
        pass


class NOAAADDSStationHelper(StationHelper):
    @staticmethod
    def get_station_from_station_id(station_id: str) -> Station:
        return Station()

    def _parse_noaa_xml(xml: str) -> Station:
        pass

    @staticmethod
    def get_station_from_lat_lon(latitude: float, longitude: float) -> Station:
        pass
