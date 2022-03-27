from enum import unique

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import mapper, relationship

from ..domain.weather.station import Station, StationHelper, StationType

metadata = MetaData()

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
# site_type: List[StationType] = field(default_factory=list)

stations = Table(
    "stations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("station_id", String(4), unique=True),
    Column("wmo_id", String(4), unique=True),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("elevation_m", Float),
    Column("site", String(255)),
    Column("state", String(2)),
    Column("country", String(2)),
)


def start_mappers():
    stations_mapper = mapper(Station, stations)
