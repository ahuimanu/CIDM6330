from weather.station import NOAAADDSStationHelper as station_helper
from weather.station import Station


def test_can_get_station_from_station_id():

    # arrange
    # act
    station = station_helper.get_station_from_station_id("XXXX")

    # assert
    assert isinstance(station, Station)
