#!/usr/bin/env python3
"""
Weather station data filtering script.

Reads weather data from CSV/JSON files, filters based on temperature threshold,
and writes results to a new file with logging.
"""

import argparse
import csv
import json
import logging
import math
from pathlib import Path
from typing import List, Dict


class WeatherFilter:
    """Filter weather station data based on temperature thresholds."""

    def __init__(self, log_file: Path):
        """Initialize the weather filter with logging configuration.

        Args:
            log_file: Path to the log file for operation logging
        """
        self.log_file = log_file
        self.records_read = 0
        self.records_written = 0
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging to write to log file in append mode."""
        # Avoid adding duplicate file handlers when running multiple times in
        # the same interpreter (e.g. in an IDE).
        logger = logging.getLogger()
        # Compare resolved absolute paths to avoid false negatives when the
        # same file is referenced via different relative paths.
        try:
            target_path = self.log_file.resolve()
        except Exception:
            target_path = self.log_file

        for h in logger.handlers:
            if not isinstance(h, logging.FileHandler):
                continue
            handler_path = getattr(h, "baseFilename", None)
            if not handler_path:
                continue
            try:
                if Path(handler_path).resolve() == target_path:
                    return
            except Exception:
                if handler_path == str(self.log_file):
                    return

        handler = logging.FileHandler(self.log_file, mode="a")
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    def _detect_format(self, input_file: Path) -> str:
        """Detect input file format based on file extension.

        Args:
            input_file: Path to the input file

        Returns:
            Format type ('csv' or 'json')

        Raises:
            ValueError: If file format is not supported
        """
        suffix = input_file.suffix.lower()
        if suffix == ".csv":
            return "csv"
        elif suffix == ".json":
            return "json"
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def read_csv(self, input_file: Path) -> List[Dict]:
        """Read CSV file and return list of records.

        Args:
            input_file: Path to CSV file

        Returns:
            List of dictionaries representing CSV rows
        """
        records = []
        with input_file.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)
                self.records_read += 1
        return records

    def read_json(self, input_file: Path) -> List[Dict]:
        """Read JSON file and return list of records.

        Args:
            input_file: Path to JSON file

        Returns:
            List of dictionaries from JSON array
        """
        with input_file.open("r", encoding="utf-8") as f:
            records = json.load(f)
            if not isinstance(records, list):
                records = [records]
            self.records_read = len(records)
        return records

    def read_data(self, input_file: Path) -> List[Dict]:
        """Read data from input file (CSV or JSON).

        Args:
            input_file: Path to input file

        Returns:
            List of dictionaries representing data records

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If file format is not supported
        """
        if not input_file.exists():
            error_msg = f"Input file not found: {input_file}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)

        file_format = self._detect_format(input_file)

        if file_format == "csv":
            records = self.read_csv(input_file)
        else:  # json
            records = self.read_json(input_file)

        logging.info(f"Read {self.records_read} records from {input_file.name}")
        return records

    def filter_by_temperature(
        self, records: List[Dict], threshold: float, mode: str = "above"
    ) -> List[Dict]:
        """Filter records by temperature threshold.

        Args:
            records: List of data records
            threshold: Temperature threshold value
            mode: Filter mode - 'above', 'below', or 'equal'

        Returns:
            Filtered list of records
        """
        filtered = []
        for record in records:
            try:
                temp = float(record.get("temperature", float("-inf")))
            except (ValueError, TypeError):
                logging.warning(
                    f"Invalid temperature value: {record.get('temperature')}"
                )
                continue

            if mode == "above" and temp >= threshold:
                filtered.append(record)
            elif mode == "below" and temp <= threshold:
                filtered.append(record)
            elif mode == "equal" and math.isclose(
                temp, threshold, rel_tol=1e-9, abs_tol=1e-6
            ):
                filtered.append(record)

        self.records_written = len(filtered)
        return filtered

    def write_csv(self, records: List[Dict], output_file: Path) -> None:
        """Write records to CSV file.

        Args:
            records: List of dictionaries to write
            output_file: Path to output CSV file
        """
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not records:
            # Create an empty file so README promise (output file created)
            # holds even when there are zero matching records.
            with output_file.open("w", encoding="utf-8"):
                pass
            logging.warning("No records to write; created empty output file")
            return

        with output_file.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

    def write_json(self, records: List[Dict], output_file: Path) -> None:
        """Write records to JSON file.

        Args:
            records: List of dictionaries to write
            output_file: Path to output JSON file
        """
        with output_file.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

    def write_data(self, records: List[Dict], output_file: Path) -> None:
        """Write data to output file (CSV or JSON).

        Args:
            records: List of dictionaries to write
            output_file: Path to output file

        Raises:
            ValueError: If file format is not supported
        """
        output_file.parent.mkdir(parents=True, exist_ok=True)

        file_format = self._detect_format(output_file)

        if file_format == "csv":
            self.write_csv(records, output_file)
        else:  # json
            self.write_json(records, output_file)

        logging.info(f"Wrote {self.records_written} records to {output_file.name}")

    def get_temperature_stats(self, records: List[Dict]) -> Dict:
        """Return basic temperature statistics for a list of records.

        Args:
            records: List of data records with a 'temperature' key

        Returns:
            Dict with keys: average, min, max, count
        """
        temps = []
        for record in records:
            try:
                temps.append(float(record["temperature"]))
            except (KeyError, ValueError, TypeError):
                continue

        if not temps:
            return {"average": None, "min": None, "max": None, "count": 0}

        return {
            "average": sum(temps) / len(temps),
            "min": min(temps),
            "max": max(temps),
            "count": len(temps),
        }

    def filter_by_station(self, records: List[Dict], station_name: str) -> List[Dict]:
        """Filter records to only those from a specific station.

        Args:
            records: List of data records
            station_name: Station name to match (case-sensitive)

        Returns:
            Filtered list of records whose 'station' field equals station_name
        """
        return [r for r in records if r.get("station") == station_name]

    def log_summary(self) -> None:
        """Log summary of operation."""
        logging.info(
            f"Operation summary: {self.records_read} read, "
            f"{self.records_written} written, "
            f"filtered {self.records_read - self.records_written} records"
        )


def main():
    """Main entry point for the weather filtering application."""
    parser = argparse.ArgumentParser(
        description="Filter weather station data by temperature threshold"
    )
    parser.add_argument("input_file", type=Path, help="Path to input CSV or JSON file")
    parser.add_argument(
        "output_file", type=Path, help="Path to output CSV or JSON file"
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        required=True,
        help="Temperature threshold for filtering",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["above", "below", "equal"],
        default="above",
        help="Filter mode: above, below, or equal threshold (default: above)",
    )
    parser.add_argument(
        "-l",
        "--log-file",
        type=Path,
        default=Path(__file__).parent / "weather_operations.log",
        help="Path to log file (default: weather_operations.log)",
    )
    import sys

    # If no CLI args provided (e.g. running in IDE), use sensible defaults for testing:
    if not sys.argv[1:]:
        script_dir = Path(__file__).parent
        default_args = [
            str(script_dir / "sample_weather_data.csv"),
            str(script_dir / "output" / "filtered_warm.csv"),
            "-t",
            "20",
            "-m",
            "above",
        ]
        print("No CLI args supplied — using defaults:", default_args)
        args = parser.parse_args(default_args)
    else:
        args = parser.parse_args()
    try:
        # Initialize filter with logging
        filter_obj = WeatherFilter(args.log_file)

        # Read data from input file
        records = filter_obj.read_data(args.input_file)

        # Filter by temperature
        filtered_records = filter_obj.filter_by_temperature(
            records, args.temperature, args.mode
        )

        # Write filtered data to output file
        filter_obj.write_data(filtered_records, args.output_file)

        # Log operation summary
        filter_obj.log_summary()

        print(
            f"✓ Processed {filter_obj.records_read} records, "
            f"wrote {filter_obj.records_written} records\n"
            f"✓ Output written to: {args.output_file}\n"
            f"✓ Log written to: {args.log_file}"
        )

    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        exit(1)
    except ValueError as e:
        print(f"✗ Error: {e}")
        exit(1)
    except Exception as e:
        logging.exception("Unexpected error during operation")
        print(f"✗ Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
