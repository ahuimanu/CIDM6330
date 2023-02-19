import pytest
from domain.weather.station import NOAAADDSStationHelper as station_helper
from domain.weather.station import Station, StationType

# tests heavily utilize the ElementTree library
# https://docs.python.org/3/library/xml.etree.elementtree.html


# https://docs.pytest.org/en/7.1.x/explanation/fixtures.html
@pytest.fixture
def xml_to_parse():
    xml_to_test = """ \
    <response xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" xsi:noNamespaceSchemaLocation="http://www.aviationweather.gov/static/adds/schema/station1_0.xsd">
    <request_index>36155907</request_index>
    <data_source name="stations"/>
    <request type="retrieve"/>
    <errors/>
    <warnings/>
    <time_taken_ms>4</time_taken_ms>
    <data num_results="1">
    <Station>
    <station_id>KAMA</station_id>
    <wmo_id>72363</wmo_id>
    <latitude>35.22</latitude>
    <longitude>-101.72</longitude>
    <elevation_m>1102.0</elevation_m>
    <site>AMARILLO</site>
    <state>TX</state>
    <country>US</country>
    <site_type>
    <METAR/>
    <NEXRAD/>
    <rawinsonde/>
    <WFO_office/>
    <TAF/>
    </site_type>
    </Station>
    </data>
    </response>
    """
    return xml_to_test


def test_can_get_xml_from_station_id():
    # arrange
    # act
    xml = station_helper._request_noaa_xml("KAMA")

    # assert
    assert len(xml) > 0


def test_can_parse_returned_noaa_xml(xml_to_parse):
    # arrange
    # act
    tree_root = station_helper._parse_noaa_xml(xml_to_parse)

    print(f"\nin parse parse_noaa_xml root tag is: {tree_root.tag}")

    # assert
    assert tree_root.tag == "response"


def test_verify_data_source(xml_to_parse):
    # arrange
    # act
    tree_root = station_helper._parse_noaa_xml(xml_to_parse)
    data_source = station_helper._get_data_source_from_xml_element(tree_root)

    # assert
    assert data_source["name"] == "stations"


def test_verify_number_of_data_records_is_one_or_more(xml_to_parse):
    # arrange
    # act
    tree_root = station_helper._parse_noaa_xml(xml_to_parse)
    data_source = station_helper._get_data_from_xml_element(tree_root)

    # https://docs.python.org/3/library/functions.html#int
    num_results = int(data_source["num_results"])

    # assert
    assert num_results >= 1


def test_can_parse_station_from_xml(xml_to_parse):
    # arrange
    tree_root = station_helper._parse_noaa_xml(xml_to_parse)
    station_element = station_helper._get_station_from_xml_element(tree_root)
    # act
    station_id = station_element[0].text
    print(station_id)

    # assert
    assert station_id == "KAMA"


def test_can_parse_site_types_from_xml(xml_to_parse):
    # arrange
    # <METAR/>
    # <NEXRAD/>
    # <rawinsonde/>
    # <WFO_office/>
    # <TAF/>
    comp_list = [
        StationType.METAR,
        StationType.NEXRAD,
        StationType.RAWINDSONDE,
        StationType.WFO_OFFICE,
        StationType.TAF,
    ]

    # print (comp_list)

    # act
    tree_root = station_helper._parse_noaa_xml(xml_to_parse)
    station_element = station_helper._get_station_from_xml_element(tree_root)
    out_list = station_helper._get_site_type_list_from_xml_element(station_element[8])

    print(out_list)

    # assert
    assert comp_list == out_list


def test_can_get_station_from_station_id():
    # arrange
    # act
    station = station_helper.get_station_from_station_id("KAMA")

    # assert
    assert isinstance(station, Station)
    assert station.station_id == "KAMA"
