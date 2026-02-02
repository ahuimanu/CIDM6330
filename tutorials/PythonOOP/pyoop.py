"""
Python OOP Comprehensive Example

This module demonstrates Python's object-oriented features using
a weather reporting domain model with airports and heliports.

Run with: python pyoop.py
Type check with: ty pyoop.py
Lint with: ruff check pyoop.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable

# =============================================================================
# PROTOCOLS - Structural Subtyping (Duck Typing with Type Hints)
# =============================================================================


@runtime_checkable
class Summarizable(Protocol):
    """Protocol for any object that can produce a summary string.

    Unlike ABCs, protocols use structural subtyping - any class with
    a matching get_summary() method satisfies this protocol without
    explicitly inheriting from it.
    """

    def get_summary(self) -> str: ...


# =============================================================================
# VALUE OBJECTS - Immutable Data with Dataclasses
# =============================================================================


@dataclass(frozen=True)
class Coordinates:
    """Immutable geographic coordinates.

    Frozen dataclasses are ideal for value objects - they're hashable,
    comparable, and can be used as dictionary keys or set members.
    """

    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        """Validate coordinates after initialization."""
        if not -90 <= self.latitude <= 90:
            raise ValueError(f"Latitude must be -90 to 90, got {self.latitude}")
        if not -180 <= self.longitude <= 180:
            raise ValueError(f"Longitude must be -180 to 180, got {self.longitude}")

    def distance_to(self, other: "Coordinates") -> float:
        """Calculate approximate distance in nautical miles (simplified)."""
        # Simplified calculation - for demo purposes
        lat_diff = abs(self.latitude - other.latitude)
        lon_diff = abs(self.longitude - other.longitude)
        return ((lat_diff**2 + lon_diff**2) ** 0.5) * 60


@dataclass
class WeatherReport:
    """Weather report data container.

    Regular dataclass (not frozen) since weather reports are mutable -
    they get updated with new data over time.
    """

    metar: str | None = None
    taf: str | None = None
    fetched_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Normalize METAR string to uppercase."""
        if self.metar:
            self.metar = self.metar.upper()

    def is_current(self, max_age_minutes: int = 60) -> bool:
        """Check if the weather report is still current."""
        age = datetime.now() - self.fetched_at
        return age.total_seconds() < max_age_minutes * 60

    @property
    def has_data(self) -> bool:
        """Check if any weather data is present."""
        return self.metar is not None or self.taf is not None


# =============================================================================
# ABSTRACT BASE CLASS - Defining the Interface
# =============================================================================


class ReportingStation(ABC):
    """Abstract base class for weather reporting stations.

    This defines the interface that all reporting stations must implement.
    You cannot instantiate this class directly - you must create a subclass
    that implements all abstract methods.
    """

    def __init__(self, stationid: str, name: str) -> None:
        """Initialize base station attributes.

        Args:
            stationid: ICAO identifier (e.g., 'KAMA')
            name: Human-readable station name
        """
        self._stationid = stationid
        self._name = name
        self._weather = WeatherReport()
        self._created_at = datetime.now()

    # -------------------------------------------------------------------------
    # Properties - Managed Attribute Access
    # -------------------------------------------------------------------------

    @property
    def stationid(self) -> str:
        """Read-only station identifier."""
        return self._stationid

    @property
    def name(self) -> str:
        """Station name with validation on set."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Station name cannot be empty")
        self._name = value.strip()

    @property
    def weather(self) -> WeatherReport:
        """Current weather report."""
        return self._weather

    @weather.setter
    def weather(self, value: WeatherReport) -> None:
        self._weather = value

    # -------------------------------------------------------------------------
    # Abstract Methods - Must Be Implemented by Subclasses
    # -------------------------------------------------------------------------

    @abstractmethod
    def get_summary(self) -> str:
        """Return a summary string describing this station.

        Each station type must provide its own implementation.
        """
        pass

    @abstractmethod
    def is_operational(self) -> bool:
        """Check if the station is currently operational."""
        pass

    @property
    @abstractmethod
    def station_type(self) -> str:
        """Return the type of station (e.g., 'airport', 'heliport')."""
        pass

    # -------------------------------------------------------------------------
    # Concrete Methods - Inherited As-Is
    # -------------------------------------------------------------------------

    def update_weather(self, metar: str | None = None, taf: str | None = None) -> None:
        """Update the weather report."""
        self._weather = WeatherReport(metar=metar, taf=taf)

    # -------------------------------------------------------------------------
    # Dunder Methods - Customize Built-in Behavior
    # -------------------------------------------------------------------------

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"{self.stationid} - {self.name}"

    def __repr__(self) -> str:
        """Unambiguous representation for debugging."""
        return f"{self.__class__.__name__}({self.stationid!r}, {self.name!r})"

    def __eq__(self, other: object) -> bool:
        """Stations are equal if they have the same ID."""
        if not isinstance(other, ReportingStation):
            return NotImplemented
        return self.stationid == other.stationid

    def __hash__(self) -> int:
        """Hash based on station ID (required since we defined __eq__)."""
        return hash(self.stationid)

    def __lt__(self, other: "ReportingStation") -> bool:
        """Enable sorting by station ID."""
        return self.stationid < other.stationid


# =============================================================================
# COMPOSITION - Runway as a Separate Class
# =============================================================================


@dataclass
class Runway:
    """Represents an airport runway.

    Demonstrates composition - Airport HAS runways rather than
    inheriting from a runway class.
    """

    identifier: str  # e.g., "04/22"
    length_ft: int
    width_ft: int
    surface: str  # e.g., "concrete", "asphalt"

    def can_support(self, min_runway_length: int) -> bool:
        """Check if runway can support aircraft requiring given length."""
        return self.length_ft >= min_runway_length

    def __str__(self) -> str:
        return (
            f"Runway {self.identifier}: {self.length_ft}x{self.width_ft}ft "
            f"({self.surface})"
        )


# =============================================================================
# CONCRETE IMPLEMENTATIONS
# =============================================================================


class Airport(ReportingStation):
    """An airport with runway information.

    Demonstrates:
    - Inheritance from abstract base class
    - Class attributes vs instance attributes
    - Composition (has runways)
    - Method overriding
    """

    # Class attribute - shared by all instances
    flight_rules: str = "FAA"

    def __init__(
        self,
        stationid: str,
        name: str,
        coordinates: Coordinates | None = None,
    ) -> None:
        """Initialize an airport.

        Args:
            stationid: ICAO identifier
            name: Airport name
            coordinates: Geographic location (optional)
        """
        super().__init__(stationid, name)
        self.coordinates = coordinates
        self._runways: list[Runway] = []  # Composition: airport HAS runways

    # -------------------------------------------------------------------------
    # Implement Abstract Methods
    # -------------------------------------------------------------------------

    def get_summary(self) -> str:
        runway_info = (
            f"{self.longest_runway}ft runway" if self._runways else "no runways"
        )
        return f"Airport {self.stationid}: {self.name} ({runway_info})"

    def is_operational(self) -> bool:
        return len(self._runways) > 0 and self.longest_runway > 0

    @property
    def station_type(self) -> str:
        return "airport"

    # -------------------------------------------------------------------------
    # Airport-Specific Methods
    # -------------------------------------------------------------------------

    @property
    def runways(self) -> list[Runway]:
        """Read-only access to runways list."""
        return self._runways.copy()

    @property
    def longest_runway(self) -> int:
        """Get the length of the longest runway in feet."""
        if not self._runways:
            return 0
        return max(r.length_ft for r in self._runways)

    def add_runway(
        self, identifier: str, length_ft: int, width_ft: int, surface: str
    ) -> None:
        """Add a runway to the airport."""
        self._runways.append(Runway(identifier, length_ft, width_ft, surface))

    def can_land(self, aircraft_min_runway: int) -> bool:
        """Check if any runway can accommodate an aircraft."""
        return any(r.can_support(aircraft_min_runway) for r in self._runways)

    # -------------------------------------------------------------------------
    # Class Methods - Alternative Constructors
    # -------------------------------------------------------------------------

    @classmethod
    def from_icao(cls, icao_code: str) -> "Airport":
        """Create an airport from just an ICAO code.

        In a real application, this would look up the airport details.
        """
        return cls(icao_code, f"Airport {icao_code}")

    # -------------------------------------------------------------------------
    # Static Methods - Utility Functions
    # -------------------------------------------------------------------------

    @staticmethod
    def validate_icao_code(code: str) -> bool:
        """Validate an ICAO airport code.

        ICAO codes are 4 uppercase letters.
        """
        return len(code) == 4 and code.isalpha() and code.isupper()


class Heliport(ReportingStation):
    """A heliport reporting station.

    Demonstrates a simpler subclass with different capabilities
    than Airport.
    """

    def __init__(self, stationid: str, name: str, has_beacon: bool) -> None:
        super().__init__(stationid, name)
        self.has_beacon = has_beacon

    def get_summary(self) -> str:
        beacon_status = "with beacon" if self.has_beacon else "no beacon"
        return f"Heliport {self.stationid}: {self.name} ({beacon_status})"

    def is_operational(self) -> bool:
        return True  # Heliports are always operational for this example

    @property
    def station_type(self) -> str:
        return "heliport"

    def is_night_capable(self) -> bool:
        """Heliports require a beacon for night operations."""
        return self.has_beacon


# =============================================================================
# MIXIN CLASSES - Add Functionality via Multiple Inheritance
# =============================================================================


class JSONMixin:
    """Mixin that adds JSON serialization capability.

    Mixins are small classes that provide specific functionality
    without being standalone. They're combined with other classes
    via multiple inheritance.
    """

    def to_dict(self) -> dict:
        """Convert public attributes to a dictionary."""
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if hasattr(value, "to_dict"):
                    result[key] = value.to_dict()
                elif isinstance(value, datetime):
                    result[key] = value.isoformat()
                elif isinstance(value, list):
                    result[key] = [
                        item.to_dict() if hasattr(item, "to_dict") else str(item)
                        for item in value
                    ]
                else:
                    result[key] = value
        return result


class AuditMixin:
    """Mixin that adds audit trail capability."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._audit_log: list[tuple[datetime, str]] = []

    def log_action(self, action: str) -> None:
        """Record an action in the audit log."""
        self._audit_log.append((datetime.now(), action))

    @property
    def audit_history(self) -> list[tuple[datetime, str]]:
        """Get the audit history."""
        return self._audit_log.copy()


class AuditableAirport(AuditMixin, Airport):
    """Airport with audit trail - demonstrates multiple inheritance."""

    def add_runway(
        self, identifier: str, length_ft: int, width_ft: int, surface: str
    ) -> None:
        super().add_runway(identifier, length_ft, width_ft, surface)
        self.log_action(f"Added runway {identifier}")

    def update_weather(self, metar: str | None = None, taf: str | None = None) -> None:
        super().update_weather(metar, taf)
        self.log_action("Weather updated")


# =============================================================================
# DEPENDENCY INJECTION - Program to Interfaces
# =============================================================================


class WeatherService(Protocol):
    """Protocol defining what a weather service must provide."""

    def fetch_metar(self, stationid: str) -> str | None: ...
    def fetch_taf(self, stationid: str) -> str | None: ...


class MockWeatherService:
    """Mock implementation for testing."""

    def __init__(
        self,
        metar: str = "VFR conditions",
        taf: str = "No significant change",
    ):
        self._metar = metar
        self._taf = taf

    def fetch_metar(self, stationid: str) -> str:
        return f"{stationid} {self._metar}"

    def fetch_taf(self, stationid: str) -> str:
        return f"{stationid} {self._taf}"


class StationManager:
    """Manages weather updates for stations.

    Demonstrates dependency injection - the weather service
    is injected, allowing for easy testing and flexibility.
    """

    def __init__(self, weather_service: WeatherService) -> None:
        self._weather_service = weather_service
        self._stations: dict[str, ReportingStation] = {}

    def register(self, station: ReportingStation) -> None:
        """Register a station for management."""
        self._stations[station.stationid] = station

    def update_all_weather(self) -> None:
        """Fetch and update weather for all registered stations."""
        for stationid, station in self._stations.items():
            metar = self._weather_service.fetch_metar(stationid)
            taf = self._weather_service.fetch_taf(stationid)
            station.update_weather(metar, taf)

    def get_station(self, stationid: str) -> ReportingStation | None:
        """Get a station by ID."""
        return self._stations.get(stationid)


# =============================================================================
# FUNCTIONS THAT WORK WITH ABSTRACTIONS
# =============================================================================


def print_station_summary(station: Summarizable) -> None:
    """Print summary for any summarizable object.

    This function works with ANY object that has a get_summary() method,
    thanks to structural subtyping via Protocol.
    """
    print(station.get_summary())


def find_nearest_airport(
    target: Coordinates, airports: list[Airport]
) -> Airport | None:
    """Find the airport nearest to a given location."""
    nearest: Airport | None = None
    min_distance = float("inf")

    for airport in airports:
        if airport.coordinates:
            distance = target.distance_to(airport.coordinates)
            if distance < min_distance:
                min_distance = distance
                nearest = airport

    return nearest


# =============================================================================
# MAIN - Demonstration
# =============================================================================


def main() -> None:  # noqa: PLR0915
    """Demonstrate Python OOP features."""

    print("=" * 70)
    print("PYTHON OOP DEMONSTRATION")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # Creating Objects
    # -------------------------------------------------------------------------

    print("\n1. CREATING OBJECTS")
    print("-" * 40)

    # Create airports with coordinates
    kama = Airport(
        stationid="KAMA",
        name="Rick Husband Amarillo International Airport",
        coordinates=Coordinates(35.2194, -101.7059),
    )
    kama.add_runway("04/22", 13502, 200, "concrete")
    kama.add_runway("13/31", 7898, 150, "asphalt")

    klbb = Airport(
        stationid="KLBB",
        name="Lubbock Preston Smith International Airport",
        coordinates=Coordinates(33.6636, -101.8228),
    )
    klbb.add_runway("17R/35L", 11500, 150, "concrete")

    kmaf = Airport.from_icao("KMAF")  # Using class method
    kmaf.name = "Midland International Air and Space Port"

    heliport = Heliport("TX07", "Northwest Texas Hospital Heliport", has_beacon=True)

    print(f"Created: {kama}")
    print(f"Created: {klbb}")
    print(f"Created: {kmaf} (from ICAO code)")
    print(f"Created: {heliport}")

    # -------------------------------------------------------------------------
    # Polymorphism
    # -------------------------------------------------------------------------

    print("\n2. POLYMORPHISM")
    print("-" * 40)

    stations: list[ReportingStation] = [kama, klbb, kmaf, heliport]

    for station in stations:
        # Same method call, different behavior based on type
        print(f"  {station.station_type}: {station.get_summary()}")

    # -------------------------------------------------------------------------
    # Using Protocols (Structural Subtyping)
    # -------------------------------------------------------------------------

    print("\n3. PROTOCOLS (DUCK TYPING)")
    print("-" * 40)

    # Weather report also satisfies Summarizable protocol (it has get_summary)
    # Actually, let's add a get_summary to WeatherReport for this demo
    class SummarizableWeather(WeatherReport):
        def get_summary(self) -> str:
            return f"Weather: {self.metar or 'No data'}"

    weather = SummarizableWeather(metar="KAMA 121755Z 36010KT 10SM CLR 25/10")

    # All these work with print_station_summary
    print("  Calling print_station_summary on different types:")
    print("  ", end="")
    print_station_summary(kama)
    print("  ", end="")
    print_station_summary(heliport)
    print("  ", end="")
    print_station_summary(weather)

    # -------------------------------------------------------------------------
    # Properties and Validation
    # -------------------------------------------------------------------------

    print("\n4. PROPERTIES")
    print("-" * 40)

    print(f"  KAMA longest runway: {kama.longest_runway}ft")
    print(f"  KAMA can land 737 (needs 6000ft): {kama.can_land(6000)}")
    print(f"  KAMA can land A380 (needs 9000ft): {kama.can_land(9000)}")

    # -------------------------------------------------------------------------
    # Composition
    # -------------------------------------------------------------------------

    print("\n5. COMPOSITION")
    print("-" * 40)

    print(f"  {kama.stationid} runways:")
    for runway in kama.runways:
        print(f"    {runway}")

    # -------------------------------------------------------------------------
    # Value Objects (Frozen Dataclass)
    # -------------------------------------------------------------------------

    print("\n6. VALUE OBJECTS")
    print("-" * 40)

    coords1 = Coordinates(35.2194, -101.7059)
    coords2 = Coordinates(35.2194, -101.7059)

    print(f"  coords1 == coords2: {coords1 == coords2}")  # True (value equality)
    print(f"  coords1 is coords2: {coords1 is coords2}")  # False (different objects)
    print(f"  Can use as dict key: {coords1 in {coords1: 'KAMA'}}")  # True (hashable)

    # -------------------------------------------------------------------------
    # Nearest Airport
    # -------------------------------------------------------------------------

    print("\n7. FINDING NEAREST AIRPORT")
    print("-" * 40)

    airports = [kama, klbb]
    target = Coordinates(34.5, -101.5)  # Somewhere between Amarillo and Lubbock

    nearest = find_nearest_airport(target, airports)
    if nearest:
        print(f"  From {target}, nearest airport is: {nearest.stationid}")

    # -------------------------------------------------------------------------
    # Dependency Injection
    # -------------------------------------------------------------------------

    print("\n8. DEPENDENCY INJECTION")
    print("-" * 40)

    # Create a mock weather service for testing
    mock_service = MockWeatherService(metar="SKC 10SM", taf="No change expected")

    # Inject it into the manager
    manager = StationManager(mock_service)
    manager.register(kama)
    manager.register(klbb)

    # Update weather using the injected service
    manager.update_all_weather()

    print(f"  KAMA weather: {kama.weather.metar}")
    print(f"  KLBB weather: {klbb.weather.metar}")

    # -------------------------------------------------------------------------
    # Multiple Inheritance with Mixins
    # -------------------------------------------------------------------------

    print("\n9. MIXINS AND MULTIPLE INHERITANCE")
    print("-" * 40)

    auditable = AuditableAirport("KDFW", "Dallas/Fort Worth International")
    auditable.add_runway("17L/35R", 13401, 200, "concrete")
    auditable.add_runway("17R/35L", 13401, 200, "concrete")
    auditable.update_weather(metar="KDFW clear skies")

    print(f"  {auditable.stationid} audit log:")
    for timestamp, action in auditable.audit_history:
        print(f"    {timestamp.strftime('%H:%M:%S')} - {action}")

    # -------------------------------------------------------------------------
    # Dunder Methods
    # -------------------------------------------------------------------------

    print("\n10. DUNDER METHODS")
    print("-" * 40)

    print(f"  str(kama): {kama!s}")
    print(f"  repr(kama): {kama!r}")
    print(f"  kama == klbb: {kama == klbb}")
    print(f"  hash(kama): {hash(kama)}")

    # Sorting uses __lt__
    sorted_stations = sorted([klbb, kama, heliport])
    print(f"  Sorted by ID: {[s.stationid for s in sorted_stations]}")

    # -------------------------------------------------------------------------
    # Class vs Instance Attributes
    # -------------------------------------------------------------------------

    print("\n11. CLASS VS INSTANCE ATTRIBUTES")
    print("-" * 40)

    print(f"  Airport.flight_rules (class): {Airport.flight_rules}")
    print(f"  kama.flight_rules (instance access): {kama.flight_rules}")

    # Modify on one instance
    kama.flight_rules = "ICAO"
    print("  After kama.flight_rules = 'ICAO':")
    print(f"    kama.flight_rules: {kama.flight_rules}")
    print(f"    klbb.flight_rules: {klbb.flight_rules}")  # Still FAA
    print(f"    Airport.flight_rules: {Airport.flight_rules}")  # Still FAA

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
