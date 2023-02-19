from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import List, TypeAlias
from urllib.error import HTTPError
from xml.etree.ElementTree import Element, fromstring

import requests
from iniconfig import ParseError


class StationType(IntEnum):
    """
    https://aviationweather.gov/dataserver/fields?datatype=station
    The station type, which can be a combination of the following:
    METAR | rawinsonde | TAF | NEXRAD | wind_profiler | WFO_office | SYNOPS

    Useful information on enums: https://betterprogramming.pub/enumerations-in-python-b01a1fb479de
    """

    METAR = 0
    RAWINDSONDE = 1
    TAF = 2
    NEXRAD = 3
    WIND_PROFILER = 4
    WFO_OFFICE = 5
    SYNOPS = 6


# https://docs.python.org/3/library/dataclasses.html#module-dataclasses
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
    site_type: List[StationType] = field(default_factory=list)

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
    NOAA_ADDS_URL = (
        f"https://aviationweather-bldr.ncep.noaa.gov/adds/dataserver_current/httpparam"
    )
    # guide url params: dataSource=stations&requestType=retrieve&format=xml&stationString=KAMA
    NOAA_ADDS_FORMAT = "xml"

    @staticmethod
    def get_station_from_station_id(station_id: str) -> Station:
        xml = NOAAADDSStationHelper._request_noaa_xml(station_id)
        tree_root = NOAAADDSStationHelper._parse_noaa_xml(xml)
        station = NOAAADDSStationHelper._create_station_from_xml_element(tree_root)

        return station

    @staticmethod
    def _create_noaa_request_uri(station_id: str) -> str:
        pass

    @staticmethod
    def _request_noaa_xml(station_id: str) -> str:
        # prepare url
        url = NOAAADDSStationHelper.NOAA_ADDS_URL
        format = NOAAADDSStationHelper.NOAA_ADDS_FORMAT

        stations_params = {
            "dataSource": "stations",
            "requestType": "retrieve",
            "format": format,
            "stationString": station_id.strip(),
        }

        # start an empty return value
        response_xml = ""

        try:
            noaa_response = requests.get(url, stations_params)
        except ConnectionError:
            response_xml = ""
        except HTTPError:
            response_xml = ""

        if noaa_response.status_code == 200:
            response_xml = noaa_response.text

        return response_xml

    def _parse_noaa_xml(xml: str) -> Element:
        # prepare - create station object
        # station_id: str = ""  # The 4-letter station specifier
        # wmo_id: str = ""  # Four-letter WMO Id for the station
        # latitude: float = 0.0  # The latitude in decimal degrees
        # longitude: float = 0.0  # The longitude in decimal degrees
        # elevation_m: float = (
        #     0.0  # The elevation of the station in MSL (above mean sea-level)
        # )
        # site: str = ""  # The "common" name/human-readable name of the station
        # state: str = (
        #     ""  # The two-letter abbreviation for the U.S. state or Canadian province
        # )
        # country: str = ""  # The two-letter country abbreviation
        # site_type: StationType = StationType.METAR

        try:
            xml_tree_root = fromstring(xml)
        except ParseError:
            xml_tree_root = None

        return xml_tree_root

    @staticmethod
    def _get_data_source_from_xml_element(xml_tree_root: Element) -> str:
        return xml_tree_root[1].attrib

    @staticmethod
    def _get_data_from_xml_element(xml_tree_root: Element) -> str:
        return xml_tree_root[6].attrib

    @staticmethod
    def _get_station_from_xml_element(xml_tree_root: Element) -> str:
        return xml_tree_root[6][0]

    @staticmethod
    def _get_site_type_list_from_xml_element(
        xml_station_root: Element,
    ) -> list(StationType):
        out_list = []

        site_types = xml_station_root
        for child in site_types:
            # METAR | rawinsonde | TAF | NEXRAD | wind_profiler | WFO_office | SYNOPS
            # https://docs.python.org/3/tutorial/controlflow.html?highlight=match#match-statements
            match child.tag:
                case "METAR":
                    out_list.append(StationType.METAR)
                case "rawinsonde":
                    out_list.append(StationType.RAWINDSONDE)
                case "TAF":
                    out_list.append(StationType.TAF)
                case "NEXRAD":
                    out_list.append(StationType.NEXRAD)
                case "wind_profiler":
                    out_list.append(StationType.WIND_PROFILER)
                case "WFO_office":
                    out_list.append(StationType.WFO_OFFICE)
                case "SYNOPS":
                    out_list.append(StationType.SYNOPS)

        return out_list

    @staticmethod
    def _create_station_from_xml_element(xml_tree_root: Element) -> Station:
        station_element = NOAAADDSStationHelper._get_station_from_xml_element(
            xml_tree_root
        )

        station_id = station_element[0].text
        wmo_id = station_element[1].text
        latitude = float(station_element[2].text)
        longitude = float(station_element[3].text)
        elevation_m = float(station_element[4].text)
        site = station_element[5].text
        state = station_element[6].text
        country = station_element[7].text
        site_type = NOAAADDSStationHelper._get_site_type_list_from_xml_element(
            station_element[8]
        )

        return Station(
            station_id,
            wmo_id,
            latitude,
            longitude,
            elevation_m,
            site,
            state,
            country,
            site_type,
        )

    @staticmethod
    def get_station_from_lat_lon(latitude: float, longitude: float) -> Station:
        pass
