# first and foremost, objects and classes are data structures and/or custom types

# if we wanted to model a weather report, we could do
from datetime import datetime
from dataclasses import dataclass

kama = [
    "stationid",
    "KAMA",
    "name",
    "Rick Husband Amarillo International Airport",
    "timestamp",
    datetime.now(),
]
klbb = [
    "stationid",
    "KLBB",
    "name",
    "Lubbock Preston Smith International Airport",
    "timestamp",
    datetime.now(),
]
klbb = [
    "stationid",
    "KMAF",
    "name",
    "Midland International Air and Space Port Airport",
    "timestamp",
    datetime.now(),
]

# the problem with this approach, and others, is that it is not self-describing
# classes can do this better

# for starters, sometimes it is useful to have a data type purposed to bundle together a few named data items.
# The idiomatic approach is to use dataclasses for this purpose


@dataclass
class WeatherReports:
    metar: str
    taf: str


class ReportingStation:
    def __init__(self, stationid, name) -> None:
        self.stationid = stationid
        self.name = name


# here we create Airport by extending ReportingStation and inheriting its properties and behaviors
class Airport(ReportingStation):
    """
    An airport modeled for utility and weather reporting
    """

    # class attribute - shared by all instances
    flight_rules = "FAA"

    # this is the constructor, it is among the build-in methods
    # called "dunder" methods for the leading and training double underscores
    # that are a unique characteristic
    def __init__(
        self,
        stationid,
        name,
        timestamp,
        longest_runway,
    ):
        super().__init__(stationid, name)
        self.timestamp = timestamp
        self.longest_runway = longest_runway

        # we would be less likely to actually accept these as arguments
        # we initialize this with no data with the understanding that we'll create valid values later
        self.weather_reports = WeatherReports(None, None)

        # the leading dunder is a signal that this is a private variable
        # there really are no private variables in python (this is just a convention)
        self.__last_updated = datetime.now()

    def __str__(self) -> str:
        return f"{self.stationid} - {self.name}"

    # instance methods
    def get_timezone_data():
        pass

    def get_summary_data():
        pass


class Heliport(ReportingStation):
    def __init__(self, stationid, name, has_beacon) -> None:
        super().__init__(stationid, name)

        self.has_beacon = has_beacon

    def get_summary_data():
        pass


# now, we assign class instances
kama = Airport(
    "KAMA", "Rick Husband Amarillo International Airport", datetime.now(), 4115
)
klbb = Airport(
    "KLBB", "Lubbock Preston Smith International Airport", datetime.now(), 3505
)
kmaf = Airport(
    "KMAF", "Midland International Air and Space Port Airport", datetime.now(), 2896
)

print(kama)
print(klbb)
print(kmaf)
