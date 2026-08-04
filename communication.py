"""
Communication Module for CanSat Ground Station.
Handles serial interface and dummy simulation mode across Linux, macOS, and Windows.
"""

import time
import random
import serial
import serial.tools.list_ports


class Communication:
    """Manages serial connection with CanSat hardware or generates simulated data."""

    def __init__(self, port: str | None = None, baudrate: int = 9600, force_dummy: bool = False):
        self.baudrate = baudrate
        self.portName = port or ""
        self.dummyPlug = force_dummy
        self.ser = serial.Serial()
        self.dummy_time_ms = 0

        if force_dummy:
            print("[Communication] Force dummy mode activated.")
            return

        available = list(serial.tools.list_ports.comports())
        print("[Communication] Available serial ports:")
        for p in available:
            print(f" - {p.device} ({p.description})")

        if not self.portName:
            if available:
                self.portName = available[0].device
                print(f"[Communication] No port specified. Selecting first available: {self.portName}")
            else:
                print("[Communication] No serial ports found. Activating dummy mode.")
                self.dummyPlug = True
                return

        try:
            self.ser = serial.Serial(self.portName, self.baudrate, timeout=0.05)
            print(f"[Communication] Connected to {self.portName} @ {self.baudrate} baud.")
        except (serial.SerialException, OSError) as e:
            print(f"[Communication] Could not open port {self.portName}: {e}")
            print("[Communication] Fallback to dummy mode.")
            self.dummyPlug = True

    @staticmethod
    def get_available_ports() -> list[str]:
        """Return a list of available serial port names across OS platforms."""
        return [p.device for p in serial.tools.list_ports.comports()]

    def close(self):
        """Close the serial port connection if active."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"[Communication] Port {self.portName} closed.")
        else:
            print(f"[Communication] Port {self.portName} is already closed or inactive.")

    def getData(self) -> list:
        """
        Read telemetry frame from serial port or generate dummy data.
        Returns a list of string/numeric values matching telemetry schema.
        """
        if not self.dummyMode():
            try:
                line = self.ser.readline()
                decoded = line.decode("utf-8", errors="ignore").strip()
                if decoded:
                    value_chain = [v.strip() for v in decoded.split(",")]
                    return value_chain
            except Exception as e:
                print(f"[Communication] Error reading serial data: {e}")
            # Fallback for empty frame or error
            return []

        # Dummy data generation
        self.dummy_time_ms += 50
        time_val = self.dummy_time_ms
        altitude_val = random.randint(0, 300)
        free_fall_val = random.getrandbits(1)
        temp_val = round(20 + random.uniform(-2, 5), 1)
        pressure_val = round(1013.25 + random.uniform(-10, 10), 1)
        gyro_pitch = round(random.uniform(-180, 180), 2)
        gyro_roll = round(random.uniform(-180, 180), 2)
        gyro_yaw = round(random.uniform(-180, 180), 2)
        acc_x = round(random.uniform(-2.0, 2.0), 2)
        acc_y = round(random.uniform(-2.0, 2.0), 2)
        acc_z = round(9.8 + random.uniform(-1.0, 1.0), 2)

        value_chain = [
            str(time_val),
            str(altitude_val),
            str(free_fall_val),
            str(temp_val),
            str(pressure_val),
            str(gyro_pitch),
            str(gyro_roll),
            str(gyro_yaw),
            str(acc_x),
            str(acc_y),
            str(acc_z),
        ]
        return value_chain

    def isOpen(self) -> bool:
        """Check if serial connection is open."""
        return self.ser.is_open if self.ser else False

    def dummyMode(self) -> bool:
        """Return True if running in dummy mode."""
        return self.dummyPlug
