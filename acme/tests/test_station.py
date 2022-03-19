from weather.station import NOAAADDSStationHelper as station_helper
from weather.station import Station


def test_can_get_xml_from_station_id():
    xml = station_helper._request_noaa_xml("KAMA")
    assert len(xml) > 0


def test_can_parse_returned_noaa_xml():
    xml_to_parse = """ \
<response xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" xsi:noNamespaceSchemaLocation="http://www.aviationweather.gov/static/adds/schema/station1_0.xsd">
<request_index>286475603</request_index>
<data_source name="stations"/>
<request type="retrieve"/>
<errors/>
<warnings/>
<time_taken_ms>3</time_taken_ms>
<data num_results="1">
<Station>
<station_id>KDEN</station_id>
<wmo_id>72565</wmo_id>
<latitude>39.85</latitude>
<longitude>-104.65</longitude>
<elevation_m>1656.0</elevation_m>
<site>DENVER (DIA)</site>
<state>CO</state>
<country>US</country>
<site_type>
<METAR/>
<TAF/>
</site_type>
</Station>
</data>
</response>
    """
    # arrange
    # act
    tree_root = station_helper._parse_noaa_xml(xml_to_parse)

    print(f"\nin parse parse_noaa_xml root tag is: {tree_root.tag}")

    assert tree_root.tag == "response"


def test_can_get_station_from_station_id():

    # arrange
    # act
    station = station_helper.get_station_from_station_id("KAMA")

    # assert
    assert isinstance(station, Station)
