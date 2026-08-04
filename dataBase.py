"""
Data Logging Module for CanSat Ground Station.
Handles CSV persistence with UTF-8 encoding and cross-platform file safety.
"""

import time
import csv
from pathlib import Path


class DataBase:
    """Manages recording telemetry data to a local CSV database file."""

    def __init__(self, filename: str | Path = "flight_data.csv"):
        self.filepath = Path(filename)
        self.state = False

    def guardar(self, data: list):
        """Append telemetry row with current timestamp if storage is active."""
        if self.state and data:
            row = list(data) + [time.strftime("%Y-%m-%d %H:%M:%S")]
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
