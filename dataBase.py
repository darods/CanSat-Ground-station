"""
Data Logging Module for CanSat Ground Station.
Handles CSV persistence with UTF-8 encoding and cross-platform file safety.
"""

import time
import csv
from pathlib import Path

# Spreadsheets execute cells that start with these characters as formulas
# (CSV formula injection). Telemetry is numeric, so a field beginning with
# them is always suspicious; prefixing a leading apostrophe forces text mode
# in Excel/Sheets. "-" is intentionally excluded because negative numbers are
# legitimate and stay numeric.
_FORMULA_PREFIXES = ("=", "+", "@")


def _neutralize_formula(value) -> str:
    """Return *value* with any spreadsheet-formula prefix neutralised."""
    stripped = str(value).lstrip()
    if stripped.startswith(_FORMULA_PREFIXES):
        return "'" + stripped
    return value


class DataBase:
    """Manages recording telemetry data to a local CSV database file."""

    def __init__(self, filename: str | Path = "flight_data.csv"):
        self.filepath = Path(filename)
        self.state = False

    def guardar(self, data: list):
        """Append telemetry row with current timestamp if storage is active."""
        if self.state and data:
            row = [_neutralize_formula(v) for v in data] + [time.strftime("%Y-%m-%d %H:%M:%S")]
            try:
                with open(self.filepath, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=",")
                    writer.writerow(row)
            except Exception as e:
                print(f"[DataBase] Error writing to CSV: {e}")

    def start(self):
        """Enable CSV data logging."""
        self.state = True
        print(f"[DataBase] CSV storage started -> {self.filepath.resolve()}")

    def stop(self):
        """Disable CSV data logging."""
        self.state = False
        print("[DataBase] CSV storage stopped.")


# Backwards compatibility alias
data_base = DataBase
