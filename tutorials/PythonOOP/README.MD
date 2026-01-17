# OOP Features in Python

Python, while being fully object-oriented, does not provide as extensive an OOP feature set as C#, Java, or C++. However, Python is still very much an OOP language. This guide covers Python's object-oriented capabilities in depth.

## Table of Contents

1. [Everything is an Object](#everything-is-an-object)
2. [Classes as Custom Types](#classes-as-custom-types)
3. [The `__init__` Constructor](#the-__init__-constructor)
4. [Instance vs Class Attributes](#instance-vs-class-attributes)
5. [Methods: Instance, Class, and Static](#methods-instance-class-and-static)
6. [Dunder (Magic) Methods](#dunder-magic-methods)
7. [Properties and Descriptors](#properties-and-descriptors)
8. [Encapsulation and Name Mangling](#encapsulation-and-name-mangling)
9. [Inheritance](#inheritance)
10. [Multiple Inheritance and the MRO](#multiple-inheritance-and-the-mro)
11. [Abstract Base Classes](#abstract-base-classes)
12. [Protocols and Structural Subtyping](#protocols-and-structural-subtyping)
13. [Dataclasses](#dataclasses)
14. [Composition vs Inheritance](#composition-vs-inheritance)
15. [SOLID Principles in Python](#solid-principles-in-python)

---

## Everything is an Object

In Python, everything is an object—integers, strings, functions, classes, and even modules. This means everything has a type, an identity, and attributes.

```python
x = 42
print(type(x))        # <class 'int'>
print(id(x))          # Memory address
print(x.bit_length()) # 6 - integers have methods!

def greet():
    """A simple greeting function."""
    return "Hello"

print(type(greet))           # <class 'function'>
print(greet.__doc__)         # A simple greeting function.
print(greet.__name__)        # greet
```

This uniformity means you can pass functions as arguments, store classes in lists, and introspect any object at runtime.

---

## Classes as Custom Types

Classes allow you to define custom data types that bundle data and behavior together. Without classes, you might model data using lists or dictionaries, but these approaches are not self-describing.

```python
# Problematic: Using lists (positional, error-prone)
kama = ["KAMA", "Rick Husband Amarillo International Airport", 4115]

# Problematic: Using dicts (better, but no type enforcement)
kama = {
    "stationid": "KAMA",
    "name": "Rick Husband Amarillo International Airport",
    "longest_runway": 4115
}

# Better: Using a class (self-describing, type-checked, has behavior)
class Airport:
    def __init__(self, stationid: str, name: str, longest_runway: int) -> None:
        self.stationid = stationid
        self.name = name
        self.longest_runway = longest_runway

kama = Airport("KAMA", "Rick Husband Amarillo International Airport", 4115)
```

Classes provide structure, documentation through type hints, and the ability to attach behavior (methods) to your data.

---

## The `__init__` Constructor

The `__init__` method is called automatically when you create an instance. It initializes the object's state. Note that `__init__` is *not* the constructor—`__new__` is. `__init__` is the *initializer*.

```python
class Airport:
    def __new__(cls, *args, **kwargs):
        """Actually creates the instance (rarely overridden)."""
        print(f"Creating instance of {cls.__name__}")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, stationid: str, name: str) -> None:
        """Initializes the instance with data."""
        print(f"Initializing {stationid}")
        self.stationid = stationid
        self.name = name

# Output:
# Creating instance of Airport
# Initializing KAMA
kama = Airport("KAMA", "Rick Husband Amarillo International Airport")
```

You almost never need to override `__new__`, but it's essential for immutable types and metaclass programming.

---

## Instance vs Class Attributes

Instance attributes belong to a specific object. Class attributes are shared across all instances.

```python
class Airport:
    # Class attribute - shared by ALL instances
    flight_rules = "FAA"
    all_airports: list["Airport"] = []  # Careful: mutable class attributes are shared!
    
    def __init__(self, stationid: str, name: str) -> None:
        # Instance attributes - unique to each instance
        self.stationid = stationid
        self.name = name
        Airport.all_airports.append(self)

kama = Airport("KAMA", "Rick Husband Amarillo International Airport")
klbb = Airport("KLBB", "Lubbock Preston Smith International Airport")

print(kama.flight_rules)  # FAA (accessed via instance)
print(Airport.flight_rules)  # FAA (accessed via class)
print(len(Airport.all_airports))  # 2 (shared across all instances)

# Instance attribute shadows class attribute
kama.flight_rules = "ICAO"
print(kama.flight_rules)  # ICAO (instance attribute)
print(klbb.flight_rules)  # FAA (still class attribute)
```

**Warning**: Mutable class attributes (like lists) are shared references. Modifying them affects all instances.

---

## Methods: Instance, Class, and Static

Python supports three types of methods, each with different binding behavior.

```python
class Airport:
    flight_rules = "FAA"
    
    def __init__(self, stationid: str, name: str) -> None:
        self.stationid = stationid
        self.name = name
    
    # Instance method: receives `self`, operates on instance data
    def get_summary(self) -> str:
        return f"{self.stationid}: {self.name}"
    
    # Class method: receives `cls`, operates on class-level data
    # Commonly used as alternative constructors
    @classmethod
    def from_icao_code(cls, icao_code: str) -> "Airport":
        """Alternative constructor using ICAO code lookup."""
        # In reality, you'd look this up
        return cls(icao_code, f"Airport {icao_code}")
    
    @classmethod
    def get_flight_rules(cls) -> str:
        return cls.flight_rules
    
    # Static method: no implicit first argument
    # Essentially a regular function namespaced to the class
    @staticmethod
    def validate_icao_code(code: str) -> bool:
        """ICAO codes are 4 uppercase letters."""
        return len(code) == 4 and code.isalpha() and code.isupper()

# Usage
kama = Airport("KAMA", "Rick Husband Amarillo International Airport")
print(kama.get_summary())  # Instance method

klbb = Airport.from_icao_code("KLBB")  # Class method as factory
print(Airport.get_flight_rules())  # Class method

print(Airport.validate_icao_code("KAMA"))  # True - static method
print(Airport.validate_icao_code("kama"))  # False
```

**When to use each**:
- **Instance methods**: Most common; need access to instance state
- **Class methods**: Alternative constructors, accessing class-level state
- **Static methods**: Utility functions logically grouped with the class

---

## Dunder (Magic) Methods

Dunder methods (double underscore) let you define how objects behave with built-in operations and functions.

```python
from datetime import datetime

class Airport:
    def __init__(self, stationid: str, name: str, longest_runway: int) -> None:
        self.stationid = stationid
        self.name = name
        self.longest_runway = longest_runway
        self._created_at = datetime.now()
    
    # String representations
    def __str__(self) -> str:
        """Human-readable string (used by print, str())."""
        return f"{self.stationid} - {self.name}"
    
    def __repr__(self) -> str:
        """Unambiguous representation (used in debugger, repr())."""
        return f"Airport({self.stationid!r}, {self.name!r}, {self.longest_runway!r})"
    
    # Comparison operators
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Airport):
            return NotImplemented
        return self.stationid == other.stationid
    
    def __lt__(self, other: "Airport") -> bool:
        """Enables sorting by runway length."""
        return self.longest_runway < other.longest_runway
    
    def __hash__(self) -> int:
        """Required if __eq__ is defined and you want to use in sets/dicts."""
        return hash(self.stationid)
    
    # Container behavior
    def __len__(self) -> int:
        """Could represent number of runways, gates, etc."""
        return self.longest_runway
    
    def __bool__(self) -> bool:
        """Truthiness - an airport is 'truthy' if it has a valid station ID."""
        return bool(self.stationid)
    
    # Attribute access
    def __getattr__(self, name: str):
        """Called when attribute is not found normally."""
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    # Context manager protocol
    def __enter__(self):
        print(f"Opening connection to {self.stationid}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing connection to {self.stationid}")
        return False  # Don't suppress exceptions

# Usage demonstrations
kama = Airport("KAMA", "Rick Husband Amarillo International Airport", 4115)
klbb = Airport("KLBB", "Lubbock Preston Smith International Airport", 3505)

print(str(kama))   # KAMA - Rick Husband Amarillo International Airport
print(repr(kama))  # Airport('KAMA', 'Rick Husband Amarillo International Airport', 4115)

print(kama == klbb)  # False
print(kama < klbb)   # False (4115 > 3505)

airports = [kama, klbb]
airports.sort()  # Uses __lt__
print([a.stationid for a in airports])  # ['KLBB', 'KAMA']

# Context manager
with kama as airport:
    print(f"Working with {airport.stationid}")
```

### Common Dunder Methods Reference

| Method | Purpose | Triggered By |
|--------|---------|--------------|
| `__init__` | Initialize instance | `ClassName()` |
| `__str__` | Human-readable string | `str()`, `print()` |
| `__repr__` | Unambiguous representation | `repr()`, debugger |
| `__eq__` | Equality comparison | `==` |
| `__lt__`, `__le__`, `__gt__`, `__ge__` | Ordering | `<`, `<=`, `>`, `>=` |
| `__hash__` | Hash value | `hash()`, dict keys, sets |
| `__len__` | Length | `len()` |
| `__bool__` | Truthiness | `bool()`, `if obj:` |
| `__getitem__`, `__setitem__` | Indexing | `obj[key]`, `obj[key] = val` |
| `__iter__`, `__next__` | Iteration | `for x in obj:` |
| `__call__` | Make instance callable | `obj()` |
| `__enter__`, `__exit__` | Context manager | `with obj:` |
| `__add__`, `__sub__`, etc. | Arithmetic | `+`, `-`, etc. |

---

## Properties and Descriptors

Properties let you define managed attributes with getter, setter, and deleter methods.

```python
class Airport:
    def __init__(self, stationid: str, name: str) -> None:
        self._stationid = stationid  # "Private" backing field
        self._name = name
    
    @property
    def stationid(self) -> str:
        """Read-only property."""
        return self._stationid
    
    @property
    def name(self) -> str:
        """Managed property with validation."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @name.deleter
    def name(self) -> None:
        raise AttributeError("Cannot delete airport name")

kama = Airport("KAMA", "Rick Husband Amarillo International Airport")

print(kama.stationid)  # KAMA
# kama.stationid = "KDFW"  # AttributeError: property 'stationid' has no setter

kama.name = "  Amarillo International  "
print(kama.name)  # "Amarillo International" (stripped)

# kama.name = ""  # ValueError: Name cannot be empty
```

### Descriptors: The Mechanism Behind Properties

Properties are implemented using the descriptor protocol. Understanding descriptors unlocks advanced patterns.

```python
class ValidatedString:
    """A descriptor that validates string values."""
    
    def __init__(self, min_length: int = 1, max_length: int = 100):
        self.min_length = min_length
        self.max_length = max_length
    
    def __set_name__(self, owner, name):
        """Called when descriptor is assigned to a class attribute."""
        self.name = name
        self.private_name = f"_{name}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)
    
    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        if not (self.min_length <= len(value) <= self.max_length):
            raise ValueError(
                f"{self.name} must be {self.min_length}-{self.max_length} characters"
            )
        setattr(obj, self.private_name, value)

class Airport:
    stationid = ValidatedString(min_length=3, max_length=4)
    name = ValidatedString(min_length=5, max_length=100)
    
    def __init__(self, stationid: str, name: str) -> None:
        self.stationid = stationid  # Validated by descriptor
        self.name = name

kama = Airport("KAMA", "Rick Husband Amarillo International Airport")
# Airport("KA", "Test")  # ValueError: stationid must be 3-4 characters
```

---

## Encapsulation and Name Mangling

Python doesn't have true private members, but uses conventions and name mangling.

```python
class Airport:
    def __init__(self, stationid: str) -> None:
        self.stationid = stationid      # Public
        self._internal = "internal"      # Protected (convention)
        self.__private = "private"       # Name-mangled
    
    def get_private(self) -> str:
        return self.__private

kama = Airport("KAMA")

print(kama.stationid)    # Public: "KAMA"
print(kama._internal)     # Accessible, but convention says "don't touch"

# print(kama.__private)   # AttributeError!
print(kama._Airport__private)  # Name-mangled: "private"
print(kama.get_private())      # Proper access: "private"
```

**Name mangling** (`__name` → `_ClassName__name`) is designed to prevent accidental override in subclasses, not for security.

```python
class Airport:
    def __init__(self):
        self.__id = 1

class InternationalAirport(Airport):
    def __init__(self):
        super().__init__()
        self.__id = 2  # This is _InternationalAirport__id, NOT _Airport__id

airport = InternationalAirport()
print(airport._Airport__id)              # 1
print(airport._InternationalAirport__id)  # 2
```

---

## Inheritance

Inheritance creates an "is-a" relationship. Subclasses inherit and can override parent behavior.

```python
from datetime import datetime
from dataclasses import dataclass

@dataclass
class WeatherReport:
    metar: str | None = None
    taf: str | None = None

class ReportingStation:
    """Base class for any station that reports weather."""
    
    def __init__(self, stationid: str, name: str) -> None:
        self.stationid = stationid
        self.name = name
        self.weather_report = WeatherReport()
    
    def get_weather(self) -> WeatherReport:
        return self.weather_report
    
    def __str__(self) -> str:
        return f"{self.stationid} - {self.name}"

class Airport(ReportingStation):
    """An airport extends ReportingStation with runway information."""
    
    flight_rules = "FAA"
    
    def __init__(
        self, 
        stationid: str, 
        name: str, 
        longest_runway: int,
        timestamp: datetime | None = None
    ) -> None:
        super().__init__(stationid, name)  # Call parent constructor
        self.longest_runway = longest_runway
        self.timestamp = timestamp or datetime.now()
    
    def can_land(self, aircraft_min_runway: int) -> bool:
        """Airport-specific method."""
        return self.longest_runway >= aircraft_min_runway

class Heliport(ReportingStation):
    """A heliport is a reporting station with beacon information."""
    
    def __init__(self, stationid: str, name: str, has_beacon: bool) -> None:
        super().__init__(stationid, name)
        self.has_beacon = has_beacon
    
    def is_night_capable(self) -> bool:
        """Heliport-specific method."""
        return self.has_beacon

# Polymorphism: different types, same interface
stations: list[ReportingStation] = [
    Airport("KAMA", "Amarillo International", 4115),
    Heliport("TX07", "Northwest Texas Hospital Heliport", True),
]

for station in stations:
    print(station)  # Uses inherited __str__
    print(station.get_weather())  # Inherited method
```

### The `super()` Function

`super()` returns a proxy object that delegates method calls to the parent class.

```python
class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        parent_greeting = super().greet()
        return f"{parent_greeting}, and B"

print(B().greet())  # "Hello from A, and B"
```

---

## Multiple Inheritance and the MRO

Python supports multiple inheritance. The Method Resolution Order (MRO) determines which method is called.

```python
class Flyable:
    def move(self) -> str:
        return "Flying"

class Drivable:
    def move(self) -> str:
        return "Driving"

class FlyingCar(Flyable, Drivable):
    pass

car = FlyingCar()
print(car.move())  # "Flying" - Flyable comes first

# View the MRO
print(FlyingCar.__mro__)
# (<class 'FlyingCar'>, <class 'Flyable'>, <class 'Drivable'>, <class 'object'>)
```

### The Diamond Problem and Cooperative Inheritance

```python
class Base:
    def __init__(self):
        print("Base.__init__")

class Left(Base):
    def __init__(self):
        print("Left.__init__")
        super().__init__()

class Right(Base):
    def __init__(self):
        print("Right.__init__")
        super().__init__()

class Diamond(Left, Right):
    def __init__(self):
        print("Diamond.__init__")
        super().__init__()

d = Diamond()
# Output:
# Diamond.__init__
# Left.__init__
# Right.__init__
# Base.__init__

print(Diamond.__mro__)
# Diamond -> Left -> Right -> Base -> object
```

**Key insight**: `super()` follows the MRO, not the class hierarchy. This enables cooperative multiple inheritance where each class calls `super()` exactly once.

### Mixins: A Pattern for Multiple Inheritance

Mixins are small classes that add specific functionality without being standalone.

```python
import json
from datetime import datetime

class JSONMixin:
    """Mixin that adds JSON serialization capability."""
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=str)
    
    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)

class TimestampMixin:
    """Mixin that adds timestamp tracking."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def touch(self):
        self.updated_at = datetime.now()

class Airport(JSONMixin, TimestampMixin):
    def __init__(self, stationid: str, name: str) -> None:
        super().__init__()  # Calls TimestampMixin.__init__
        self.stationid = stationid
        self.name = name

kama = Airport("KAMA", "Amarillo International")
print(kama.to_json())  # From JSONMixin
print(kama.created_at)  # From TimestampMixin
```

---

## Abstract Base Classes

Abstract base classes (ABCs) define interfaces that subclasses must implement.

```python
from abc import ABC, abstractmethod
from datetime import datetime

class ReportingStation(ABC):
    """Abstract base class for all reporting stations."""
    
    def __init__(self, stationid: str, name: str) -> None:
        self.stationid = stationid
        self.name = name
    
    @abstractmethod
    def get_summary(self) -> str:
        """Subclasses must implement this."""
        pass
    
    @abstractmethod
    def is_operational(self) -> bool:
        """Subclasses must implement this."""
        pass
    
    # Concrete method - inherited as-is
    def __str__(self) -> str:
        return f"{self.stationid} - {self.name}"

class Airport(ReportingStation):
    def __init__(self, stationid: str, name: str, longest_runway: int) -> None:
        super().__init__(stationid, name)
        self.longest_runway = longest_runway
    
    def get_summary(self) -> str:
        return f"Airport {self.stationid} with {self.longest_runway}ft runway"
    
    def is_operational(self) -> bool:
        return self.longest_runway > 0

# station = ReportingStation("TEST", "Test")  # TypeError: Can't instantiate abstract class
kama = Airport("KAMA", "Amarillo International", 4115)
print(kama.get_summary())
```

### Abstract Properties

```python
from abc import ABC, abstractmethod

class ReportingStation(ABC):
    @property
    @abstractmethod
    def station_type(self) -> str:
        """Each station must declare its type."""
        pass

class Airport(ReportingStation):
    @property
    def station_type(self) -> str:
        return "airport"
```

---

## Protocols and Structural Subtyping

Protocols (PEP 544) enable "duck typing" with static type checking—structural subtyping rather than nominal subtyping.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Summarizable(Protocol):
    """Any object with a get_summary method."""
    
    def get_summary(self) -> str:
        ...

class Airport:
    def __init__(self, stationid: str, name: str) -> None:
        self.stationid = stationid
        self.name = name
    
    def get_summary(self) -> str:
        return f"Airport: {self.stationid}"

class WeatherReport:
    def __init__(self, metar: str) -> None:
        self.metar = metar
    
    def get_summary(self) -> str:
        return f"Weather: {self.metar}"

def print_summary(item: Summarizable) -> None:
    """Works with ANY object that has get_summary()."""
    print(item.get_summary())

# Both work - no inheritance required!
print_summary(Airport("KAMA", "Amarillo"))
print_summary(WeatherReport("KAMA 121755Z 36010KT"))

# Runtime checking
print(isinstance(Airport("KAMA", "Test"), Summarizable))  # True
```

**Protocols vs ABCs**:
- **ABCs**: Nominal subtyping—classes must explicitly inherit
- **Protocols**: Structural subtyping—classes just need matching methods

---

## Dataclasses

Dataclasses reduce boilerplate for classes that primarily store data.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class WeatherReport:
    metar: str
    taf: str | None = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Post-init processing
    def __post_init__(self):
        self.metar = self.metar.upper()

@dataclass(frozen=True)  # Immutable
class Coordinates:
    latitude: float
    longitude: float

@dataclass(order=True)  # Enables comparison operators
class Airport:
    # sort_index is used for ordering but excluded from repr
    sort_index: int = field(init=False, repr=False)
    stationid: str
    name: str
    longest_runway: int
    coordinates: Coordinates | None = None
    
    def __post_init__(self):
        self.sort_index = self.longest_runway

# Automatic __init__, __repr__, __eq__
kama = Airport("KAMA", "Amarillo International", 4115)
klbb = Airport("KLBB", "Lubbock International", 3505)

print(kama)  # Airport(stationid='KAMA', name='Amarillo International', longest_runway=4115, coordinates=None)
print(kama == klbb)  # False
print(kama > klbb)   # True (by runway length)

# Frozen dataclass
coords = Coordinates(35.2194, -101.7059)
# coords.latitude = 36.0  # FrozenInstanceError
```

### Dataclass Field Options

| Option | Purpose |
|--------|---------|
| `default` | Default value |
| `default_factory` | Callable for mutable defaults |
| `init` | Include in `__init__` |
| `repr` | Include in `__repr__` |
| `compare` | Include in comparisons |
| `hash` | Include in `__hash__` |
| `field(...)` | Configure individual fields |

---

## Composition vs Inheritance

Favor composition over inheritance when possible. Composition creates a "has-a" relationship.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class WeatherReport:
    metar: str | None = None
    taf: str | None = None
    fetched_at: datetime = field(default_factory=datetime.now)
    
    def is_current(self, max_age_minutes: int = 60) -> bool:
        age = datetime.now() - self.fetched_at
        return age.total_seconds() < max_age_minutes * 60

@dataclass
class Runway:
    identifier: str
    length_ft: int
    surface: str
    
    def can_support(self, aircraft_min_runway: int) -> bool:
        return self.length_ft >= aircraft_min_runway

@dataclass
class Airport:
    stationid: str
    name: str
    runways: list[Runway] = field(default_factory=list)
    weather: WeatherReport = field(default_factory=WeatherReport)
    
    @property
    def longest_runway(self) -> int:
        if not self.runways:
            return 0
        return max(r.length_ft for r in self.runways)
    
    def add_runway(self, identifier: str, length_ft: int, surface: str) -> None:
        self.runways.append(Runway(identifier, length_ft, surface))

# Composition in action
kama = Airport("KAMA", "Amarillo International")
kama.add_runway("04/22", 13502, "concrete")
kama.add_runway("13/31", 7898, "asphalt")
kama.weather = WeatherReport(metar="KAMA 121755Z 36010KT 10SM CLR 25/10 A3012")

print(kama.longest_runway)  # 13502
print(kama.weather.is_current())  # True (just created)
```

**When to use inheritance**:
- True "is-a" relationship
- Polymorphism is needed
- Extending framework classes

**When to use composition**:
- "Has-a" relationship
- Flexibility to change components at runtime
- Avoiding deep inheritance hierarchies

---

## SOLID Principles in Python

### Single Responsibility Principle

A class should have one reason to change.

```python
# Bad: Airport does too many things
class Airport:
    def __init__(self, stationid: str):
        self.stationid = stationid
    
    def fetch_weather(self): ...
    def save_to_database(self): ...
    def render_html(self): ...

# Good: Separate responsibilities
class Airport:
    def __init__(self, stationid: str, name: str):
        self.stationid = stationid
        self.name = name

class WeatherService:
    def fetch(self, airport: Airport) -> WeatherReport: ...

class AirportRepository:
    def save(self, airport: Airport) -> None: ...

class AirportRenderer:
    def to_html(self, airport: Airport) -> str: ...
```

### Open/Closed Principle

Open for extension, closed for modification.

```python
from abc import ABC, abstractmethod

class NotificationSender(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

class EmailSender(NotificationSender):
    def send(self, message: str) -> None:
        print(f"Email: {message}")

class SMSSender(NotificationSender):
    def send(self, message: str) -> None:
        print(f"SMS: {message}")

# Adding new notification types doesn't modify existing code
class PushSender(NotificationSender):
    def send(self, message: str) -> None:
        print(f"Push: {message}")
```

### Liskov Substitution Principle

Subtypes must be substitutable for their base types.

```python
class Bird:
    def move(self) -> str:
        return "Moving"

class Sparrow(Bird):
    def move(self) -> str:
        return "Flying"

class Penguin(Bird):
    def move(self) -> str:
        return "Swimming"  # Still valid - penguins move, just differently

# Both work wherever Bird is expected
def make_bird_move(bird: Bird) -> str:
    return bird.move()
```

### Interface Segregation Principle

Clients shouldn't depend on interfaces they don't use.

```python
from typing import Protocol

# Bad: One fat interface
class AirportOperations(Protocol):
    def get_weather(self) -> str: ...
    def process_passengers(self) -> None: ...
    def handle_cargo(self) -> None: ...
    def manage_fuel(self) -> None: ...

# Good: Segregated interfaces
class WeatherReporter(Protocol):
    def get_weather(self) -> str: ...

class PassengerHandler(Protocol):
    def process_passengers(self) -> None: ...

class CargoHandler(Protocol):
    def handle_cargo(self) -> None: ...
```

### Dependency Inversion Principle

Depend on abstractions, not concretions.

```python
from typing import Protocol

class WeatherService(Protocol):
    def fetch(self, stationid: str) -> str: ...

class NOAAWeatherService:
    def fetch(self, stationid: str) -> str:
        return f"NOAA weather for {stationid}"

class MockWeatherService:
    def fetch(self, stationid: str) -> str:
        return "Mock weather data"

class Airport:
    def __init__(self, stationid: str, weather_service: WeatherService) -> None:
        self.stationid = stationid
        self._weather_service = weather_service  # Injected dependency
    
    def get_weather(self) -> str:
        return self._weather_service.fetch(self.stationid)

# Production
real_airport = Airport("KAMA", NOAAWeatherService())

# Testing
test_airport = Airport("KAMA", MockWeatherService())
```

---

## Complete Example

Bringing it all together:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

# Protocols for duck typing
class Summarizable(Protocol):
    def get_summary(self) -> str: ...

# Value objects as frozen dataclasses
@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float

@dataclass
class WeatherReport:
    metar: str | None = None
    taf: str | None = None
    fetched_at: datetime = field(default_factory=datetime.now)

# Abstract base class defining the interface
class ReportingStation(ABC):
    def __init__(self, stationid: str, name: str) -> None:
        self.stationid = stationid
        self.name = name
        self.weather = WeatherReport()
    
    @abstractmethod
    def get_summary(self) -> str:
        pass
    
    def __str__(self) -> str:
        return f"{self.stationid} - {self.name}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.stationid!r}, {self.name!r})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ReportingStation):
            return NotImplemented
        return self.stationid == other.stationid
    
    def __hash__(self) -> int:
        return hash(self.stationid)

# Concrete implementations
class Airport(ReportingStation):
    flight_rules: str = "FAA"
    
    def __init__(
        self,
        stationid: str,
        name: str,
        longest_runway: int,
        coordinates: Coordinates | None = None
    ) -> None:
        super().__init__(stationid, name)
        self.longest_runway = longest_runway
        self.coordinates = coordinates
    
    def get_summary(self) -> str:
        return f"Airport {self.stationid}: {self.name} ({self.longest_runway}ft runway)"

class Heliport(ReportingStation):
    def __init__(self, stationid: str, name: str, has_beacon: bool) -> None:
        super().__init__(stationid, name)
        self.has_beacon = has_beacon
    
    def get_summary(self) -> str:
        beacon = "with beacon" if self.has_beacon else "no beacon"
        return f"Heliport {self.stationid}: {self.name} ({beacon})"

# Functions work with abstractions
def print_station_summary(station: Summarizable) -> None:
    print(station.get_summary())

# Usage
if __name__ == "__main__":
    stations: list[ReportingStation] = [
        Airport(
            "KAMA",
            "Rick Husband Amarillo International Airport",
            13502,
            Coordinates(35.2194, -101.7059)
        ),
        Airport(
            "KLBB",
            "Lubbock Preston Smith International Airport",
            11500
        ),
        Heliport(
            "TX07",
            "Northwest Texas Hospital Heliport",
            True
        ),
    ]
    
    for station in stations:
        print_station_summary(station)
```

---

## Further Reading

- [Python Data Model](https://docs.python.org/3/reference/datamodel.html) - Official documentation on special methods
- [PEP 544 - Protocols](https://peps.python.org/pep-0544/) - Structural subtyping
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/) - Dataclass specification
- [Fluent Python, 2nd Edition](https://www.oreilly.com/library/view/fluent-python-2nd/9781492056348/) - Deep dive into Python's object model
