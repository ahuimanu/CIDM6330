# File Handling and Serialization in Python

This guide covers reading and writing files, working with common data formats, and serializing Python objects for persistence. These are foundational operations for any application that needs to store or exchange data.

## Table of Contents

1. [Pathlib: Modern File Paths](#pathlib-modern-file-paths)
2. [Reading and Writing Text Files](#reading-and-writing-text-files)
3. [Context Managers and Resource Safety](#context-managers-and-resource-safety)
4. [Working with CSV](#working-with-csv)
5. [Working with JSON](#working-with-json)
6. [Working with YAML](#working-with-yaml)
7. [Serialization Patterns](#serialization-patterns)
8. [Binary Files and Pickle](#binary-files-and-pickle)
9. [File System Operations](#file-system-operations)
10. [Best Practices](#best-practices)

---

## Pathlib: Modern File Paths

The `pathlib` module (Python 3.4+) provides an object-oriented interface for filesystem paths. It replaces the older `os.path` module for most use cases.

```python
from pathlib import Path

# Creating paths
current_dir = Path(".")
home = Path.home()
config_file = Path("/etc/config.yaml")

# Path from current file's location
here = Path(__file__).parent
data_dir = here / "data"

# Building paths with / operator (cross-platform!)
airports_file = data_dir / "airports" / "kama.json"

# Path properties
print(airports_file.name)       # kama.json
print(airports_file.stem)       # kama
print(airports_file.suffix)     # .json
print(airports_file.parent)     # data/airports
print(airports_file.parts)      # ('data', 'airports', 'kama.json')

# Absolute vs relative
print(airports_file.is_absolute())  # False
print(airports_file.absolute())     # /full/path/to/data/airports/kama.json
print(airports_file.resolve())      # Resolves symlinks too

# Checking existence and type
if airports_file.exists():
    print(airports_file.is_file())  # True
    print(airports_file.is_dir())   # False
```

### Why Pathlib Over os.path?

```python
import os.path
from pathlib import Path

# Old way (os.path) - string manipulation, verbose
old_path = os.path.join(os.path.dirname(__file__), "data", "airports.csv")
old_name = os.path.basename(old_path)
old_exists = os.path.exists(old_path)

# New way (pathlib) - object-oriented, readable
new_path = Path(__file__).parent / "data" / "airports.csv"
new_name = new_path.name
new_exists = new_path.exists()

# Pathlib methods return Path objects, enabling chaining
config = Path.home() / ".config" / "myapp"
config.mkdir(parents=True, exist_ok=True)
```

---

## Reading and Writing Text Files

### Basic Reading

```python
from pathlib import Path

# Read entire file as string
content = Path("airports.txt").read_text()

# Read with specific encoding (always be explicit!)
content = Path("airports.txt").read_text(encoding="utf-8")

# Read as list of lines
lines = Path("airports.txt").read_text(encoding="utf-8").splitlines()

# Read with file handle (for large files or line-by-line processing)
with open("airports.txt", "r", encoding="utf-8") as f:
    for line in f:  # Memory efficient - one line at a time
        print(line.strip())
```

### Basic Writing

```python
from pathlib import Path

# Write entire string (overwrites existing content)
Path("output.txt").write_text("KAMA,Amarillo\nKLBB,Lubbock\n", encoding="utf-8")

# Write with file handle (more control)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("KAMA,Amarillo\n")
    f.write("KLBB,Lubbock\n")

# Append to existing file
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("KMAF,Midland\n")

# Write multiple lines
lines = ["KAMA,Amarillo", "KLBB,Lubbock", "KMAF,Midland"]
Path("output.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
```

### File Modes Reference

| Mode | Description |
|------|-------------|
| `r` | Read (default) |
| `w` | Write (truncates existing) |
| `a` | Append |
| `x` | Exclusive create (fails if exists) |
| `b` | Binary mode (e.g., `rb`, `wb`) |
| `+` | Read and write (e.g., `r+`) |

---

## Context Managers and Resource Safety

Context managers ensure files are properly closed, even if exceptions occur. This connects directly to the `__enter__` and `__exit__` dunder methods from OOP.

```python
# ALWAYS use context managers for file operations
with open("airports.txt", "r", encoding="utf-8") as f:
    content = f.read()
# File is automatically closed here, even if an exception occurred

# BAD: Manual open/close (what if an exception happens?)
f = open("airports.txt", "r")
content = f.read()
f.close()  # May never execute if read() raises!

# Multiple files in one context
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    for line in infile:
        outfile.write(line.upper())
```

### Creating Your Own Context Manager

```python
from contextlib import contextmanager
from pathlib import Path
import tempfile
import shutil

@contextmanager
def temporary_directory():
    """Context manager that creates a temp directory and cleans it up."""
    temp_dir = Path(tempfile.mkdtemp())
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

# Usage
with temporary_directory() as temp:
    data_file = temp / "airports.json"
    data_file.write_text('{"stationid": "KAMA"}')
    # Work with temp files...
# Directory and all contents automatically deleted
```

---

## Working with CSV

CSV (Comma-Separated Values) is ubiquitous for tabular data exchange.

### Reading CSV

```python
import csv
from pathlib import Path

# Basic reading with DictReader (recommended)
with open("airports.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['stationid']}: {row['name']}")

# Reading into a list
with open("airports.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    airports = list(reader)

# Basic reader (returns lists, not dicts)
with open("airports.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip header row
    for row in reader:
        stationid, name, runway_length = row
        print(f"{stationid}: {name}")
```

### Writing CSV

```python
import csv

airports = [
    {"stationid": "KAMA", "name": "Amarillo International", "runway_ft": 13502},
    {"stationid": "KLBB", "name": "Lubbock International", "runway_ft": 11500},
    {"stationid": "KMAF", "name": "Midland International", "runway_ft": 9501},
]

# Writing with DictWriter (recommended)
with open("airports.csv", "w", encoding="utf-8", newline="") as f:
    fieldnames = ["stationid", "name", "runway_ft"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(airports)

# Writing with basic writer
with open("airports.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["stationid", "name", "runway_ft"])  # Header
    writer.writerow(["KAMA", "Amarillo International", 13502])
    writer.writerow(["KLBB", "Lubbock International", 11500])
```

### CSV Dialects and Options

```python
import csv

# Tab-separated values
with open("airports.tsv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f, delimiter="\t")
    airports = list(reader)

# Custom dialect
with open("airports.csv", "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(
        f,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
    )
    airports = list(reader)

# Handle different line endings and quotes
csv.register_dialect(
    "custom",
    delimiter="|",
    quotechar="'",
    quoting=csv.QUOTE_NONNUMERIC,
)
```

**Important**: Always use `newline=""` when opening CSV files. This prevents issues with line endings across platforms.

---

## Working with JSON

JSON (JavaScript Object Notation) is the standard for web APIs and configuration files.

### Reading JSON

```python
import json
from pathlib import Path

# Read from file
with open("airports.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# One-liner with pathlib
data = json.loads(Path("airports.json").read_text(encoding="utf-8"))

# Parse JSON string
json_string = '{"stationid": "KAMA", "name": "Amarillo International"}'
airport = json.loads(json_string)
print(airport["stationid"])  # KAMA
```

### Writing JSON

```python
import json
from pathlib import Path

airport = {
    "stationid": "KAMA",
    "name": "Amarillo International",
    "runways": [
        {"id": "04/22", "length_ft": 13502},
        {"id": "13/31", "length_ft": 7898},
    ],
}

# Write to file (compact)
with open("airport.json", "w", encoding="utf-8") as f:
    json.dump(airport, f)

# Write to file (human-readable)
with open("airport.json", "w", encoding="utf-8") as f:
    json.dump(airport, f, indent=2)

# One-liner with pathlib
Path("airport.json").write_text(
    json.dumps(airport, indent=2),
    encoding="utf-8"
)

# Convert to string
json_string = json.dumps(airport, indent=2)
```

### JSON Serialization Options

```python
import json
from datetime import datetime
from dataclasses import dataclass, asdict

# Problem: datetime is not JSON serializable
data = {"timestamp": datetime.now()}
# json.dumps(data)  # TypeError!

# Solution 1: Custom encoder
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps(data, cls=DateTimeEncoder)

# Solution 2: default function
json.dumps(data, default=str)  # Converts anything unknown to string

# Solution 3: Pre-process with dataclass
@dataclass
class Airport:
    stationid: str
    name: str
    
    def to_dict(self) -> dict:
        return asdict(self)

airport = Airport("KAMA", "Amarillo International")
json.dumps(airport.to_dict())
```

### JSON Best Practices

```python
import json

# Ensure ASCII off for international characters
data = {"city": "Zürich"}
json.dumps(data, ensure_ascii=False)  # {"city": "Zürich"}
json.dumps(data)  # {"city": "Z\u00fcrich"}

# Sort keys for deterministic output (useful for diffs)
json.dumps(data, sort_keys=True)

# Compact separators for smaller files
json.dumps(data, separators=(",", ":"))  # No spaces
```

---

## Working with YAML

YAML (YAML Ain't Markup Language) is popular for configuration files due to its readability. It requires the `pyyaml` package.

```bash
uv add pyyaml
```

### Reading YAML

```python
import yaml
from pathlib import Path

# Read from file
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# One-liner with pathlib
config = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))

# Parse YAML string
yaml_string = """
airports:
  - stationid: KAMA
    name: Amarillo International
  - stationid: KLBB
    name: Lubbock International
"""
data = yaml.safe_load(yaml_string)
```

### Writing YAML

```python
import yaml
from pathlib import Path

config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "airports",
    },
    "airports": [
        {"stationid": "KAMA", "name": "Amarillo International"},
        {"stationid": "KLBB", "name": "Lubbock International"},
    ],
}

# Write to file
with open("config.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, default_flow_style=False)

# Output:
# airports:
# - name: Amarillo International
#   stationid: KAMA
# - name: Lubbock International
#   stationid: KLBB
# database:
#   host: localhost
#   name: airports
#   port: 5432

# Control output style
yaml.dump(config, f, default_flow_style=False, sort_keys=False, indent=2)
```

### YAML vs JSON

| Feature | JSON | YAML |
|---------|------|------|
| Comments | No | Yes (`# comment`) |
| Readability | Good | Excellent |
| Data types | Limited | Rich (dates, etc.) |
| Whitespace | Ignored | Significant |
| Stdlib | Yes | No (needs pyyaml) |
| Use case | APIs, data exchange | Configuration |

**Security Warning**: Always use `yaml.safe_load()`, never `yaml.load()`. The unsafe loader can execute arbitrary Python code!

---

## Serialization Patterns

Serialization converts Python objects to a format that can be stored or transmitted. This bridges OOP and persistence.

### Pattern 1: to_dict / from_dict

The most common and flexible pattern—explicit control over serialization.

```python
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class WeatherReport:
    stationid: str
    metar: str
    timestamp: datetime
    
    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "stationid": self.stationid,
            "metar": self.metar,
            "timestamp": self.timestamp.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "WeatherReport":
        """Deserialize from dictionary."""
        return cls(
            stationid=data["stationid"],
            metar=data["metar"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )
    
    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> "WeatherReport":
        """Deserialize from JSON string."""
        return cls.from_dict(json.loads(json_str))

# Usage
report = WeatherReport("KAMA", "KAMA 121755Z 36010KT 10SM CLR", datetime.now())

# Round-trip through JSON
json_str = report.to_json()
restored = WeatherReport.from_json(json_str)
assert report.stationid == restored.stationid
```

### Pattern 2: Protocol-Based Serialization

Define a protocol for serializable objects.

```python
from typing import Protocol, TypeVar, Type
import json

T = TypeVar("T")

class Serializable(Protocol):
    def to_dict(self) -> dict: ...
    
    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T: ...

def save_json(obj: Serializable, path: str) -> None:
    """Save any serializable object to JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj.to_dict(), f, indent=2)

def load_json(cls: Type[T], path: str) -> T:
    """Load a serializable object from JSON."""
    with open(path, "r", encoding="utf-8") as f:
        return cls.from_dict(json.load(f))

# Usage with any class that implements the protocol
save_json(report, "report.json")
restored = load_json(WeatherReport, "report.json")
```

### Pattern 3: Dataclass with asdict

Quick serialization for simple dataclasses (no custom datetime handling).

```python
from dataclasses import dataclass, asdict, fields
import json

@dataclass
class Runway:
    identifier: str
    length_ft: int
    surface: str

@dataclass 
class Airport:
    stationid: str
    name: str
    runways: list[Runway]
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Airport":
        # Handle nested dataclasses
        runways = [Runway(**r) for r in data.pop("runways", [])]
        return cls(**data, runways=runways)

airport = Airport(
    "KAMA", 
    "Amarillo International",
    [Runway("04/22", 13502, "concrete")]
)

# asdict handles nested dataclasses automatically
print(json.dumps(airport.to_dict(), indent=2))
```

---

## Binary Files and Pickle

For Python-specific object persistence, `pickle` serializes objects to bytes.

```python
import pickle
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Airport:
    stationid: str
    name: str
    last_updated: datetime

airport = Airport("KAMA", "Amarillo International", datetime.now())

# Save with pickle
with open("airport.pkl", "wb") as f:
    pickle.dump(airport, f)

# Load with pickle
with open("airport.pkl", "rb") as f:
    restored = pickle.load(f)

# One-liners
Path("airport.pkl").write_bytes(pickle.dumps(airport))
restored = pickle.loads(Path("airport.pkl").read_bytes())
```

### Pickle Caveats

**Security**: Never unpickle untrusted data! Pickle can execute arbitrary code.

```python
# DANGEROUS - could execute malicious code
data = get_data_from_untrusted_source()
obj = pickle.loads(data)  # DON'T DO THIS
```

**Compatibility**: Pickled objects may not load if:
- Python version changes significantly
- Class definition changes (added/removed attributes)
- Module is renamed or moved

**When to Use Pickle**:
- Caching computed results
- Inter-process communication (within your system)
- Quick prototyping

**When to Use JSON/YAML Instead**:
- Data exchange with other systems
- Human-readable configuration
- Long-term storage
- Untrusted data sources

---

## File System Operations

Beyond reading and writing, `pathlib` provides comprehensive filesystem operations.

```python
from pathlib import Path
import shutil

# Directory operations
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)  # Create if doesn't exist
data_dir.mkdir(parents=True, exist_ok=True)  # Create parent dirs too

# List directory contents
for item in data_dir.iterdir():
    print(f"{item.name}: {'dir' if item.is_dir() else 'file'}")

# Glob patterns
for json_file in data_dir.glob("*.json"):
    print(f"Found: {json_file}")

# Recursive glob
for json_file in data_dir.glob("**/*.json"):
    print(f"Found (recursive): {json_file}")

# File operations
source = Path("airports.json")
dest = Path("backup/airports.json")

dest.parent.mkdir(parents=True, exist_ok=True)

# Copy
shutil.copy(source, dest)  # Copy file
shutil.copytree(data_dir, Path("backup/data"))  # Copy directory

# Move/rename
source.rename(dest)  # Move or rename

# Delete
Path("temp.txt").unlink(missing_ok=True)  # Delete file
shutil.rmtree(Path("temp_dir"))  # Delete directory tree

# File metadata
if source.exists():
    print(f"Size: {source.stat().st_size} bytes")
    print(f"Modified: {source.stat().st_mtime}")
```

### Temporary Files and Directories

```python
import tempfile
from pathlib import Path

# Temporary file (auto-deleted when closed)
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    f.write('{"test": true}')
    temp_path = Path(f.name)

# Temporary directory
with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    data_file = temp_path / "data.json"
    data_file.write_text('{"test": true}')
    # Directory and contents deleted when context exits
```

---

## Best Practices

### 1. Always Specify Encoding

```python
# BAD - uses system default encoding (varies by platform)
with open("file.txt", "r") as f:
    content = f.read()

# GOOD - explicit UTF-8
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
```

### 2. Use Pathlib for Paths

```python
# BAD - string concatenation
path = "data" + "/" + "airports" + "/" + "kama.json"

# GOOD - pathlib
path = Path("data") / "airports" / "kama.json"
```

### 3. Always Use Context Managers

```python
# BAD - manual close
f = open("file.txt")
data = f.read()
f.close()

# GOOD - context manager
with open("file.txt") as f:
    data = f.read()
```

### 4. Handle Missing Files Gracefully

```python
from pathlib import Path
import json

def load_config(path: Path) -> dict:
    """Load config, returning defaults if file doesn't exist."""
    if not path.exists():
        return {"default": True}
    
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")
```

### 5. Use Type Hints for Serialization

```python
from typing import TypeVar, Type
import json

T = TypeVar("T")

def load_json_as(cls: Type[T], path: str) -> T:
    """Load JSON and convert to specified class."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return cls.from_dict(data)
```

### 6. Validate Data on Load

```python
@dataclass
class Airport:
    stationid: str
    name: str
    
    @classmethod
    def from_dict(cls, data: dict) -> "Airport":
        # Validate required fields
        if "stationid" not in data:
            raise ValueError("Missing required field: stationid")
        if "name" not in data:
            raise ValueError("Missing required field: name")
        
        # Validate data types/formats
        if not data["stationid"].isupper():
            raise ValueError(f"Invalid stationid: {data['stationid']}")
        
        return cls(
            stationid=data["stationid"],
            name=data["name"],
        )
```

---

## Further Reading

- [pathlib documentation](https://docs.python.org/3/library/pathlib.html)
- [csv module documentation](https://docs.python.org/3/library/csv.html)
- [json module documentation](https://docs.python.org/3/library/json.html)
- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Real Python: Working With Files in Python](https://realpython.com/working-with-files-in-python/)
