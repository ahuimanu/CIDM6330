<<<<<<< HEAD
# CIDM6330-Spring2026-Test-Tester

Test-Tester

I am starting out on the right foot, as well. 
=======
# Weather Station Data Filter

A Python command-line tool for filtering weather station data by temperature thresholds. Supports both CSV and JSON input/output formats with comprehensive logging.

## Features

- **CSV and JSON Support**: Automatically detects input format by file extension
- **Temperature Filtering**: Filter records above, below, or equal to a specified threshold
- **Pathlib Integration**: Uses `pathlib.Path` for all file operations
- **Context Managers**: Proper resource management with `with` statements
- **Logging**: Append-mode logging of all operations with timestamps
- **Error Handling**: Graceful handling of missing files and invalid data
- **Command-Line Interface**: Flexible argument parsing with argparse

## Requirements

- Python 3.7+

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd CIDM6330-Kata_Repo

# Create virtual environment (optional but recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

## Usage

```bash
python weather_filter.py <input_file> <output_file> -t <temperature> [OPTIONS]
```

### Arguments

- `input_file`: Path to input CSV or JSON file (required)
- `output_file`: Path to output CSV or JSON file (required)
- `-t, --temperature`: Temperature threshold (required, float)
- `-m, --mode`: Filter mode - 'above' (≥), 'below' (≤), or 'equal' (=) (default: above)
- `-l, --log-file`: Path to log file (default: weather_operations.log)
- `-h, --help`: Show help message

### Examples

#### Filter CSV: Records with temperature ≥ 50°F
```bash
python weather_filter.py sample_weather_data.csv output/warm.csv -t 50
```

#### Filter CSV to JSON: Records with temperature ≤ 30°F
```bash
python weather_filter.py sample_weather_data.csv output/cold.json -t 30 -m below
```

#### Filter JSON: Records with temperature = 72.5°F
```bash
python weather_filter.py sample_weather_data.json output/exact.csv -t 72.5 -m equal
```

#### Custom log file
```bash
python weather_filter.py input.csv output.csv -t 50 -l custom.log
```

## Input Data Format

### CSV Format
```csv
station_id,station_name,temperature,humidity,pressure,observation_date
NOAA001,Boston Logan,32.5,65,30.12,2026-01-25
NOAA002,New York LaGuardia,28.3,72,29.95,2026-01-25
```

### JSON Format
```json
[
  {
    "station_id": "NOAA001",
    "station_name": "Boston Logan",
    "temperature": 32.5,
    "humidity": 65,
    "pressure": 30.12,
    "observation_date": "2026-01-25"
  }
]
```

## Output Format

Output files are created in the same format as the requested output file extension (`.csv` or `.json`). Parent directories are created automatically if they don't exist.

## Running in an IDE / Default arguments

If the script is run without any command-line arguments (for example, run from an IDE), it will use sensible defaults for quick testing:

```
sample_weather_data.csv output/filtered_warm.csv -t 20 -m above
```

This behavior is implemented so you can quickly run the script during development. To run with custom files and options, provide the normal CLI arguments as shown above.

## Logging

All operations are logged to the specified log file (default: `weather_operations.log`) in append mode. Each log entry includes:
- Timestamp
- Log level (INFO/ERROR)
- Operation details (records read, records written, etc.)

Example log output:
```
2026-01-29 22:05:18 - INFO - Read 20 records from sample_weather_data.csv
2026-01-29 22:05:18 - INFO - Wrote 5 records to filtered_warm.csv
2026-01-29 22:05:18 - INFO - Operation summary: 20 read, 5 written, filtered 15 records
```

## Error Handling

The script handles errors gracefully:
- **Missing input file**: Reports file not found and exits with code 1
- **Invalid format**: Rejects unsupported file formats
- **Invalid temperature values**: Skips records with malformed temperature data with warnings
- **I/O errors**: Logs exceptions and reports to user

## Implementation Details

### Key Design Patterns

1. **Pathlib**: All file paths use `pathlib.Path` for cross-platform compatibility
2. **Context Managers**: File handling via `with` statements ensures proper resource cleanup
3. **Type Hints**: Full type annotations for better code clarity and IDE support
4. **Separation of Concerns**: `WeatherFilter` class encapsulates all filtering logic
5. **Format Detection**: Automatic format detection based on file extension

### Class Structure

- **`WeatherFilter`**: Main filtering engine
  - `read_data()`: Unified interface for reading CSV or JSON
  - `filter_by_temperature()`: Core filtering logic
  - `write_data()`: Unified interface for writing CSV or JSON
  - `log_summary()`: Records operation statistics

## Testing

Sample NOAA weather data is included:
- `sample_weather_data.csv`: 20 weather stations in CSV format
- `sample_weather_data.json`: Same data in JSON format

Test various filtering scenarios:
```bash
# Test above threshold
python weather_filter.py sample_weather_data.csv output/warm.csv -t 50

# Test below threshold
python weather_filter.py sample_weather_data.json output/cold.json -t 30 -m below

# Test CSV to JSON conversion
python weather_filter.py sample_weather_data.csv output/converted.json -t 40

# Test JSON to CSV conversion
python weather_filter.py sample_weather_data.json output/converted.csv -t 40
```

## Project Structure

```
CIDM6330-Kata_Repo/
├── weather_filter.py              # Main script
├── sample_weather_data.csv        # Sample data (CSV)
├── sample_weather_data.json       # Sample data (JSON)
├── weather_operations.log         # Log file (created on first run)
├── output/                        # Output directory (created by script)
│   ├── filtered_warm.csv
│   ├── filtered_cold.json
│   └── ...
├── .gitignore                     # Git ignore file
└── README.md                      # This file
```

## License

Open source - Educational kata project
>>>>>>> 9742e5e (Add comprehensive README documentation)
