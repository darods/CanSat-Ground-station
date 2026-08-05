"""
Communication Module for the CanSat Ground Station.

Responsibilities
----------------
* Open / close the serial port that links the ground station to the CanSat
  (or OBC) telemetry link, on Linux, macOS and Windows.
* Parse the comma-separated telemetry frames received over the wire.
* When no hardware is available (or ``--dummy`` is passed), synthesize a
  physically plausible sub-orbital flight profile so the whole GUI can be
  exercised end to end without any sensors connected. The simulated mission
  covers motor burn, a ballistic coast to apogee (weightlessness / free fall,
  the "orbit-like" part), a ballistic descent capped at terminal velocity and
  finally a parachute descent back to the pad. The battery drains as the
  mission progresses.
"""

import math
import random
import time

import serial
import serial.tools.list_ports

# --- Dummy-mode flight profile constants --------------------------------
# A realistic sounding-rocket trajectory for a CanSat:
GRAVITY = 9.81          # m/s²
THRUST_ACC = 80.0       # net upward acceleration while the motor burns (m/s²)
T_THRUST = 3.0          # seconds the motor burns
CHUTE_DROP_S = 12.0     # seconds of ballistic free fall before the parachute opens
TERMINAL_V = 45.0       # terminal velocity cap during ballistic descent (m/s)
CHUTE_SINK = 8.0        # vertical descent rate under parachute (m/s)

# Derived flight times / heights (constant, computed once).
_BURNOUT_V = THRUST_ACC * T_THRUST                       # speed at motor burnout
_T_APOGEE = T_THRUST + _BURNOUT_V / GRAVITY              # time of maximum altitude
_H_APOGEE = 0.5 * THRUST_ACC * T_THRUST**2 + _BURNOUT_V**2 / (2 * GRAVITY)
_T_CHUTE = _T_APOGEE + CHUTE_DROP_S                      # parachute deploy time
_FALL_DIST = min(0.5 * GRAVITY * CHUTE_DROP_S**2, TERMINAL_V * CHUTE_DROP_S)
_H_CHUTE = max(0.0, _H_APOGEE - _FALL_DIST)              # altitude at deploy
_T_LAND = _T_CHUTE + _H_CHUTE / CHUTE_SINK               # touchdown time


class Communication:
    """Manages the serial connection with the CanSat or generates simulated data."""

    def __init__(self, port: str | None = None, baudrate: int = 9600, force_dummy: bool = False):
        self.baudrate = baudrate
        self.portName = port or ""
        self.dummyPlug = force_dummy
        self.ser = serial.Serial()
        self._dummy_start = None  # monotonic clock reference for the simulator
        self._battery_drain = 0.0  # accumulated battery drain during the mission
        self._last_sim_t = None  # last mission time, to accumulate drain correctly

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
        Read one telemetry frame from the serial port or generate simulated data.

        Returns a list of string/numeric values matching the telemetry schema:
        [0] elapsed ms, [1] altitude m, [2] free-fall flag, [3] temp °C,
        [4] pressure hPa, [5] gyro pitch, [6] gyro roll, [7] gyro yaw,
        [8..10] accel X/Y/Z, [11] battery % (dummy mode only).
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

        # ---- Dummy / simulation path ----
        # Base the mission clock on the real wall clock so the displayed time
        # advances 1:1 with wall-clock time regardless of the update interval.
        if self._dummy_start is None:
            self._dummy_start = time.monotonic()
        elapsed_s = time.monotonic() - self._dummy_start
        elapsed_ms = elapsed_s * 1000.0

        state = self._flight_state(elapsed_s)

        # Barometric formula: pressure as a function of altitude.
        pressure = 1013.25 * (1.0 - 2.25577e-5 * state["alt"]) ** 5.25588

        # Standard atmospheric lapse rate: cooler the higher you go.
        temperature = 15.0 - 0.0065 * state["alt"]

        # Attitude rates depend on the flight phase: the rocket spins up
        # during the burn and settles down afterwards.
        if state["motor_on"]:
            gyro_pitch = random.uniform(-2.0, 2.0) + 1.5 * math.sin(3.0 * elapsed_s)
            gyro_roll = random.uniform(2.0, 6.0)  # spin-up during burn
            gyro_yaw = random.uniform(-2.0, 2.0)
        else:
            gyro_pitch = random.uniform(-1.0, 1.0)
            gyro_roll = random.uniform(-1.5, 1.5)
            gyro_yaw = random.uniform(-1.0, 1.0)

        # Accelerometer readings: strong vibration during the burn, near
        # weightlessness (micro-gravity) while coasting / in free fall,
        # reduced by drag under the parachute and 1 g on the ground.
        if state["motor_on"]:
            acc_x = random.uniform(-0.6, 0.6)
            acc_y = random.uniform(-0.6, 0.6)
            acc_z = state["accel_z"] + random.uniform(-1.5, 1.5)
        elif state["free_fall"]:
            acc_x = random.uniform(-0.05, 0.05)
            acc_y = random.uniform(-0.05, 0.05)
            acc_z = state["accel_z"] + random.uniform(-0.05, 0.05)
        elif state["alt"] <= 0:
            acc_x = random.uniform(-0.02, 0.02)  # sitting on the pad / landed
            acc_y = random.uniform(-0.02, 0.02)
            acc_z = GRAVITY + random.uniform(-0.02, 0.02)
        else:
            acc_x = random.uniform(-0.15, 0.15)  # descending under parachute
            acc_y = random.uniform(-0.15, 0.15)
            acc_z = state["accel_z"] + random.uniform(-0.3, 0.3)

        # Battery: integrate the drain over time so it is always monotonic.
        # Baseline consumption is ~1.2 %/min, with extra draw while the motor
        # is powered. The accumulator makes the drop steady and visible.
        if self._last_sim_t is not None:
            dt = elapsed_s - self._last_sim_t
            self._battery_drain += (dt / 60.0) * 1.2
            if state["motor_on"]:
                self._battery_drain += dt * 0.15
        self._last_sim_t = elapsed_s
        battery = max(0.0, min(100.0, 100.0 - self._battery_drain))

        return [
            str(round(elapsed_ms, 1)),
            str(round(state["alt"], 1)),
            str(state["free_fall"]),
            str(round(temperature + random.uniform(-0.5, 0.5), 1)),
            str(round(pressure + random.uniform(-0.4, 0.4), 1)),
            str(round(gyro_pitch, 2)),
            str(round(gyro_roll, 2)),
            str(round(gyro_yaw, 2)),
            str(round(acc_x, 2)),
            str(round(acc_y, 2)),
            str(round(acc_z, 2)),
            str(round(battery, 1)),
        ]

    def _flight_state(self, t: float) -> dict:
        """Return the physical state of the simulated vehicle at time ``t`` (s)."""
        state = {"alt": 0.0, "free_fall": 0, "accel_z": GRAVITY, "motor_on": False}

        if t < 0:
            # Pre-launch: sitting on the pad.
            state["accel_z"] = GRAVITY
        elif t < T_THRUST:
            # Motor burn: strong upward acceleration plus g on the sensor.
            state["motor_on"] = True
            state["alt"] = 0.5 * THRUST_ACC * t * t
            state["accel_z"] = THRUST_ACC + GRAVITY
        elif t < _T_APOGEE:
            # Coasting up after burnout: ballistic, engines off, weightless.
            dt = t - T_THRUST
            state["alt"] = 0.5 * THRUST_ACC * T_THRUST**2 + _BURNOUT_V * dt - 0.5 * GRAVITY * dt * dt
            state["accel_z"] = 0.0
            state["free_fall"] = 1
        elif t < _T_CHUTE:
            # Ballistic descent below apogee: still in free fall.
            dt = t - _T_APOGEE
            fall = min(0.5 * GRAVITY * dt * dt, TERMINAL_V * dt)
            state["alt"] = max(0.0, _H_APOGEE - fall)
            state["accel_z"] = 0.0
            state["free_fall"] = 1
        elif t < _T_LAND:
            # Parachute descent: drag limits the speed, specific force < g.
            dt = t - _T_CHUTE
            state["alt"] = max(0.0, _H_CHUTE - CHUTE_SINK * dt)
            state["accel_z"] = GRAVITY - 1.3
            state["free_fall"] = 0
        else:
            # Landed: back on the pad, reading 1 g again.
            state["alt"] = 0.0
            state["accel_z"] = GRAVITY

        return state

    def isOpen(self) -> bool:
        """Check if serial connection is open."""
        return self.ser.is_open if self.ser else False

    def dummyMode(self) -> bool:
        """Return True if running in dummy mode."""
        return self.dummyPlug
