"""
File Handling and Serialization Example

This module demonstrates Python's file handling capabilities using
a weather reporting domain model with airports and weather data.

Run with: python example.py
"""

import csv
import json
import tempfile
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Protocol, TypeVar

# Optional: YAML support (install with: uv add pyyaml)
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# =============================================================================
# DOMAIN MODELS WITH SERIALIZATION
# =============================================================================


@dataclass
class Runway:
    """Airport runway with serialization support."""

    identifier: str
    length_ft: int
    width_ft: int
    surface: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Runway":
        return cls(**data)


@dataclass
class WeatherReport:
    """Weather report with timestamp handling for serialization."""

    metar: str | None = None
    taf: str | None = None
    fetched_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "metar": self.metar,
            "taf": self.taf,
            "fetched_at": self.fetched_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WeatherReport":
        fetched_at = data.get("fetched_at")
        if isinstance(fetched_at, str):
            fetched_at = datetime.fromisoformat(fetched_at)
        elif fetched_at is None:
            fetched_at = datetime.now()

        return cls(
            metar=data.get("metar"),
            taf=data.get("taf"),
            fetched_at=fetched_at,
        )


@dataclass
class Airport:
    """Airport with full serialization support for multiple formats."""

    stationid: str
    name: str
    city: str
    state: str
    runways: list[Runway] = field(default_factory=list)
    weather: WeatherReport = field(default_factory=WeatherReport)

    # -------------------------------------------------------------------------
    # Serialization Methods
    # -------------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON/YAML serialization."""
        return {
            "stationid": self.stationid,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "runways": [r.to_dict() for r in self.runways],
            "weather": self.weather.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Airport":
        """Create from dictionary (JSON/YAML deserialization)."""
        runways = [Runway.from_dict(r) for r in data.get("runways", [])]
        weather_data = data.get("weather", {})
        weather = (
            WeatherReport.from_dict(weather_data) if weather_data else WeatherReport()
        )

        return cls(
            stationid=data["stationid"],
            name=data["name"],
            city=data.get("city", ""),
            state=data.get("state", ""),
            runways=runways,
            weather=weather,
        )

    def to_csv_row(self) -> dict:
        """Convert to flat dictionary for CSV (no nested structures)."""
        return {
            "stationid": self.stationid,
            "name": self.name,
            "city": self.city,
            "state": self.state,
            "runway_count": len(self.runways),
            "longest_runway_ft": max((r.length_ft for r in self.runways), default=0),
            "metar": self.weather.metar or "",
        }

    @classmethod
    def from_csv_row(cls, row: dict) -> "Airport":
        """Create from CSV row (flat structure, no runways)."""
        weather = WeatherReport(metar=row.get("metar") or None)
        return cls(
            stationid=row["stationid"],
            name=row["name"],
            city=row.get("city", ""),
            state=row.get("state", ""),
            weather=weather,
        )

    # -------------------------------------------------------------------------
    # JSON Convenience Methods
    # -------------------------------------------------------------------------

    def to_json(self, indent: int | None = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> "Airport":
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))

    def save_json(self, path: Path) -> None:
        """Save to JSON file."""
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load_json(cls, path: Path) -> "Airport":
        """Load from JSON file."""
        return cls.from_json(path.read_text(encoding="utf-8"))


# =============================================================================
# SERIALIZATION PROTOCOL
# =============================================================================


T = TypeVar("T")


class Serializable(Protocol):
    """Protocol for objects that can be serialized to/from dict."""

    def to_dict(self) -> dict: ...

    @classmethod
    def from_dict(cls: type[T], data: dict) -> T: ...


def save_as_json(obj: Serializable, path: Path) -> None:
    """Save any serializable object to JSON file."""
    path.write_text(json.dumps(obj.to_dict(), indent=2), encoding="utf-8")


def load_from_json(cls: type[T], path: Path) -> T:
    """Load a serializable object from JSON file."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return cls.from_dict(data)


# =============================================================================
# CSV UTILITIES
# =============================================================================


def save_airports_csv(airports: list[Airport], path: Path) -> None:
    """Save airports to CSV file."""
    if not airports:
        return

    fieldnames = [
        "stationid",
        "name",
        "city",
        "state",
        "runway_count",
        "longest_runway_ft",
        "metar",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for airport in airports:
            writer.writerow(airport.to_csv_row())


def load_airports_csv(path: Path) -> list[Airport]:
    """Load airports from CSV file."""
    airports = []

    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            airports.append(Airport.from_csv_row(row))

    return airports


# =============================================================================
# YAML UTILITIES
# =============================================================================


def save_airports_yaml(airports: list[Airport], path: Path) -> None:
    """Save airports to YAML file."""
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML not installed. Run: uv add pyyaml")

    data = {"airports": [a.to_dict() for a in airports]}

    with path.open("w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def load_airports_yaml(path: Path) -> list[Airport]:
    """Load airports from YAML file."""
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML not installed. Run: uv add pyyaml")

    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return [Airport.from_dict(a) for a in data.get("airports", [])]


# =============================================================================
# CONTEXT MANAGER FOR TEMPORARY WORKSPACE
# =============================================================================


@contextmanager
def temporary_workspace():
    """Context manager providing a temporary directory for file operations."""
    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = Path(temp_dir)
        print(f"  Created temporary workspace: {workspace}")
        yield workspace
        print("  Cleaned up temporary workspace")


# =============================================================================
# CONFIGURATION FILE EXAMPLE
# =============================================================================


@dataclass
class AppConfig:
    """Application configuration with file persistence."""

    database_path: str = "airports.db"
    cache_ttl_seconds: int = 3600
    log_level: str = "INFO"
    enabled_stations: list[str] = field(
        default_factory=lambda: [
            "KAMA",
            "KLBB",
            "KMAF",
        ]
    )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AppConfig":
        return cls(**data)

    @classmethod
    def load(cls, path: Path) -> "AppConfig":
        """Load config from file, or return defaults if not found."""
        if not path.exists():
            return cls()

        suffix = path.suffix.lower()
        content = path.read_text(encoding="utf-8")

        if suffix == ".json":
            return cls.from_dict(json.loads(content))
        elif suffix in (".yaml", ".yml"):
            if not YAML_AVAILABLE:
                raise ImportError("PyYAML required for .yaml files")
            return cls.from_dict(yaml.safe_load(content))
        else:
            raise ValueError(f"Unsupported config format: {suffix}")

    def save(self, path: Path) -> None:
        """Save config to file (format determined by extension)."""
        suffix = path.suffix.lower()

        if suffix == ".json":
            content = json.dumps(self.to_dict(), indent=2)
        elif suffix in (".yaml", ".yml"):
            if not YAML_AVAILABLE:
                raise ImportError("PyYAML required for .yaml files")
            content = yaml.dump(self.to_dict(), default_flow_style=False)
        else:
            raise ValueError(f"Unsupported config format: {suffix}")

        path.write_text(content, encoding="utf-8")


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================


def main() -> None:  # noqa: PLR0915
    """Demonstrate file handling and serialization features."""

    print("=" * 70)
    print("FILE HANDLING AND SERIALIZATION DEMONSTRATION")
    print("=" * 70)

    # Create sample data
    airports = [
        Airport(
            stationid="KAMA",
            name="Rick Husband Amarillo International Airport",
            city="Amarillo",
            state="TX",
            runways=[
                Runway("04/22", 13502, 200, "concrete"),
                Runway("13/31", 7898, 150, "asphalt"),
            ],
            weather=WeatherReport(metar="KAMA 121755Z 36010KT 10SM CLR 25/10 A3012"),
        ),
        Airport(
            stationid="KLBB",
            name="Lubbock Preston Smith International Airport",
            city="Lubbock",
            state="TX",
            runways=[
                Runway("17R/35L", 11500, 150, "concrete"),
                Runway("17L/35R", 8000, 150, "asphalt"),
            ],
            weather=WeatherReport(metar="KLBB 121755Z 35008KT 10SM FEW250 24/08 A3015"),
        ),
        Airport(
            stationid="KMAF",
            name="Midland International Air and Space Port",
            city="Midland",
            state="TX",
            runways=[
                Runway("10/28", 9501, 150, "concrete"),
            ],
        ),
    ]

    with temporary_workspace() as workspace:
        # ---------------------------------------------------------------------
        # 1. PATHLIB BASICS
        # ---------------------------------------------------------------------

        print("\n1. PATHLIB BASICS")
        print("-" * 40)

        data_dir = workspace / "data"
        data_dir.mkdir(exist_ok=True)

        json_dir = data_dir / "json"
        json_dir.mkdir(exist_ok=True)

        print("  Created directory structure:")
        print(f"    {data_dir}")
        print(f"    {json_dir}")

        # Path properties
        sample_path = json_dir / "airports.json"
        print(f"\n  Path properties for {sample_path.name}:")
        print(f"    .name:   {sample_path.name}")
        print(f"    .stem:   {sample_path.stem}")
        print(f"    .suffix: {sample_path.suffix}")
        print(f"    .parent: {sample_path.parent.name}")

        # ---------------------------------------------------------------------
        # 2. TEXT FILE OPERATIONS
        # ---------------------------------------------------------------------

        print("\n2. TEXT FILE OPERATIONS")
        print("-" * 40)

        text_file = workspace / "stations.txt"

        # Write lines
        lines = [f"{a.stationid}: {a.name}" for a in airports]
        text_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  Wrote {len(lines)} lines to {text_file.name}")

        # Read and display
        content = text_file.read_text(encoding="utf-8")
        print("  Content:")
        for line in content.strip().split("\n"):
            print(f"    {line}")

        # ---------------------------------------------------------------------
        # 3. CSV OPERATIONS
        # ---------------------------------------------------------------------

        print("\n3. CSV OPERATIONS")
        print("-" * 40)

        csv_file = data_dir / "airports.csv"

        # Save to CSV
        save_airports_csv(airports, csv_file)
        print(f"  Saved {len(airports)} airports to {csv_file.name}")

        # Show CSV content
        print("  CSV content:")
        csv_content = csv_file.read_text(encoding="utf-8")
        for line in csv_content.strip().split("\n")[:4]:  # Header + 3 rows
            print(f"    {line[:70]}...")

        # Load from CSV
        loaded_csv = load_airports_csv(csv_file)
        print(f"  Loaded {len(loaded_csv)} airports from CSV")

        # ---------------------------------------------------------------------
        # 4. JSON OPERATIONS
        # ---------------------------------------------------------------------

        print("\n4. JSON OPERATIONS")
        print("-" * 40)

        # Save individual airport
        kama_file = json_dir / "kama.json"
        airports[0].save_json(kama_file)
        print(f"  Saved KAMA to {kama_file.name}")

        # Show JSON content
        print("  JSON content (truncated):")
        json_content = kama_file.read_text(encoding="utf-8")
        for line in json_content.split("\n")[:10]:
            print(f"    {line}")
        print("    ...")

        # Load from JSON
        loaded_kama = Airport.load_json(kama_file)
        print(f"  Loaded: {loaded_kama.stationid} - {loaded_kama.name}")
        print(f"  Runways preserved: {len(loaded_kama.runways)}")
        print(f"  Weather preserved: {loaded_kama.weather.metar is not None}")

        # Save all airports as JSON array
        all_airports_file = json_dir / "all_airports.json"
        all_data = {"airports": [a.to_dict() for a in airports]}
        all_airports_file.write_text(json.dumps(all_data, indent=2), encoding="utf-8")
        print(f"\n  Saved all airports to {all_airports_file.name}")

        # ---------------------------------------------------------------------
        # 5. YAML OPERATIONS
        # ---------------------------------------------------------------------

        print("\n5. YAML OPERATIONS")
        print("-" * 40)

        if YAML_AVAILABLE:
            yaml_file = data_dir / "airports.yaml"

            # Save to YAML
            save_airports_yaml(airports, yaml_file)
            print(f"  Saved {len(airports)} airports to {yaml_file.name}")

            # Show YAML content
            print("  YAML content (truncated):")
            yaml_content = yaml_file.read_text(encoding="utf-8")
            for line in yaml_content.split("\n")[:15]:
                print(f"    {line}")
            print("    ...")

            # Load from YAML
            loaded_yaml = load_airports_yaml(yaml_file)
            print(f"  Loaded {len(loaded_yaml)} airports from YAML")
        else:
            print("  PyYAML not installed. Skipping YAML demo.")
            print("  Install with: uv add pyyaml")

        # ---------------------------------------------------------------------
        # 6. CONFIGURATION FILES
        # ---------------------------------------------------------------------

        print("\n6. CONFIGURATION FILES")
        print("-" * 40)

        # Create and save config
        config = AppConfig(
            database_path="data/airports.db",
            cache_ttl_seconds=1800,
            log_level="DEBUG",
            enabled_stations=["KAMA", "KLBB", "KMAF", "KDFW"],
        )

        config_json = workspace / "config.json"
        config.save(config_json)
        print(f"  Saved config to {config_json.name}")
        print("  Content:")
        for line in config_json.read_text().split("\n"):
            print(f"    {line}")

        # Load config
        loaded_config = AppConfig.load(config_json)
        print("\n  Loaded config:")
        print(f"    database_path: {loaded_config.database_path}")
        print(f"    cache_ttl_seconds: {loaded_config.cache_ttl_seconds}")
        print(f"    log_level: {loaded_config.log_level}")
        print(f"    enabled_stations: {loaded_config.enabled_stations}")

        # Load missing config (returns defaults)
        missing_config = AppConfig.load(workspace / "missing.json")
        print("\n  Missing config returns defaults:")
        print(f"    database_path: {missing_config.database_path}")

        # ---------------------------------------------------------------------
        # 7. DIRECTORY OPERATIONS
        # ---------------------------------------------------------------------

        print("\n7. DIRECTORY OPERATIONS")
        print("-" * 40)

        print(f"  Contents of {data_dir.name}/:")
        for item in sorted(data_dir.iterdir()):
            item_type = "dir" if item.is_dir() else "file"
            size = item.stat().st_size if item.is_file() else 0
            print(f"    {item.name:<20} ({item_type}, {size} bytes)")

        # Glob for JSON files
        print("\n  All JSON files (recursive glob):")
        for json_file in sorted(workspace.glob("**/*.json")):
            relative = json_file.relative_to(workspace)
            print(f"    {relative}")

        # ---------------------------------------------------------------------
        # 8. SERIALIZATION ROUND-TRIP VERIFICATION
        # ---------------------------------------------------------------------

        print("\n8. SERIALIZATION ROUND-TRIP VERIFICATION")
        print("-" * 40)

        original = airports[0]

        # JSON round-trip
        json_str = original.to_json()
        from_json = Airport.from_json(json_str)

        print(
            f"  Original:   {original.stationid} with {len(original.runways)} runways"
        )
        print(
            f"  From JSON:  {from_json.stationid} with {len(from_json.runways)} runways"
        )
        print(f"  Match: {original.stationid == from_json.stationid}")
        runway_match = original.runways[0].length_ft == from_json.runways[0].length_ft
        print(f"  Runway match: {runway_match}")

        # Verify datetime round-trip
        original_time = original.weather.fetched_at
        restored_time = from_json.weather.fetched_at
        print(f"  Datetime preserved: {original_time == restored_time}")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
