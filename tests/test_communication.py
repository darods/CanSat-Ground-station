"""
Unit tests for the telemetry communication layer (``communication.py``).

The dummy-mode flight simulator is the most modified piece of this tool, so
these tests pin down its *contract*:

* the frame structure / field types the rest of the app relies on,
* the physical behaviour of the simulated sub-orbital flight profile,
* the monotonic battery drain,
* the real-time mission clock,
* the serial frame validation used to skip malformed first frames.

To sample the simulator at an arbitrary mission time ``t`` the tests
fast-forward the internal monotonic clock (``frame_at``). The simulator is
otherwise deterministic enough to assert on.
"""

import math
import time

import pytest

import communication as comm_module
from communication import Communication

# Frame indexes (must match the schema documented in README.md).
(
    I_TIME,
    I_ALT,
    I_FF,
    I_TEMP,
    I_PRESS,
    I_PITCH,
    I_ROLL,
    I_YAW,
    I_AX,
    I_AY,
    I_AZ,
    I_BATT,
) = range(12)


def frame_at(comm: Communication, t: float) -> list:
    """Sample the dummy simulator at mission time ``t`` (seconds)."""
    comm._dummy_start = time.monotonic() - t
    comm._last_sim_t = None
    comm._battery_drain = 0.0
    return comm.getData()


def run_mission(
    comm: Communication, duration_s: float, step: float = 0.05, start: float = 0.0
) -> list:
    """Simulate ``duration_s`` of a mission starting at mission time ``start``.

    ``getData`` accumulates the battery drain across calls, so a mission has
    to be simulated call-by-call for the battery tests to be meaningful.
    Pass ``start`` to sample a specific phase (e.g. ``start=10`` skips the
    motor burn).
    """
    comm._dummy_start = time.monotonic() - start
    comm._battery_drain = 0.0
    comm._last_sim_t = None
    frames = []
    t = start
    while t <= start + duration_s:
        frames.append(comm.getData())
        comm._dummy_start = time.monotonic() - t  # fast-forward virtual clock
        t += step
    return frames


@pytest.fixture
def comm():
    return Communication(force_dummy=True)


# --------------------------------------------------------------------------- #
# Frame structure
# --------------------------------------------------------------------------- #
def test_dummy_frame_has_all_fields(comm):
    frame = comm.getData()
    assert len(frame) == 12


def test_dummy_frame_values_are_strings(comm):
    assert all(isinstance(v, str) for v in comm.getData())


def test_dummy_frame_is_numeric(comm):
    frame = frame_at(comm, 10.0)
    for v in frame:
        float(v)  # raises ValueError if not numeric


def test_dummy_mode_flags(comm):
    assert comm.dummyMode() is True
    assert comm.isOpen() is False


# --------------------------------------------------------------------------- #
# Flight profile: the four phases
# --------------------------------------------------------------------------- #
def test_thrust_phase_physics(comm):
    t = 1.5  # mid-burn
    state = comm._flight_state(t)
    assert state["motor_on"] is True
    assert state["free_fall"] == 0
    # h = 0.5 * a * t^2, specific force = a + g
    assert state["alt"] == pytest.approx(0.5 * 80.0 * t**2, rel=1e-3)
    assert state["accel_z"] == pytest.approx(80.0 + 9.81, rel=1e-3)


def test_coast_phase_is_weightless(comm):
    state = comm._flight_state(10.0)
    assert state["motor_on"] is False
    assert state["free_fall"] == 1
    assert state["accel_z"] == pytest.approx(0.0, abs=1e-6)


def test_apogee_height_and_time(comm):
    state = comm._flight_state(comm_module._T_APOGEE)
    assert state["alt"] == pytest.approx(comm_module._H_APOGEE, rel=1e-3)


def test_ballistic_descent_is_free_fall(comm):
    state = comm._flight_state(comm_module._T_APOGEE + 5.0)
    assert state["free_fall"] == 1
    assert state["accel_z"] == pytest.approx(0.0, abs=1e-6)


def test_parachute_phase(comm):
    state = comm._flight_state(comm_module._T_CHUTE + 5.0)
    assert state["free_fall"] == 0
    # Under the parachute drag reduces the specific force below 1 g.
    assert state["accel_z"] == pytest.approx(9.81 - 1.3, rel=1e-3)
    assert 0.0 < state["alt"] < comm_module._H_CHUTE


def test_landed_phase(comm):
    state = comm._flight_state(comm_module._T_LAND + 10.0)
    assert state["alt"] == 0.0
    assert state["accel_z"] == pytest.approx(9.81, rel=1e-3)
    assert state["free_fall"] == 0


def test_altitude_never_negative(comm):
    for t in range(0, 500, 5):
        assert comm._flight_state(t)["alt"] >= 0.0


# --------------------------------------------------------------------------- #
# Derived channels: pressure and temperature follow altitude
# --------------------------------------------------------------------------- #
def test_pressure_decreases_with_altitude(comm):
    low = float(frame_at(comm, 2.0)[I_PRESS])  # near the pad
    high = float(frame_at(comm, comm_module._T_APOGEE)[I_PRESS])
    assert low > high


def test_temperature_decreases_with_altitude(comm):
    low = float(frame_at(comm, 2.0)[I_TEMP])
    high = float(frame_at(comm, comm_module._T_APOGEE)[I_TEMP])
    assert low > high


# --------------------------------------------------------------------------- #
# Battery
# --------------------------------------------------------------------------- #
def test_battery_monotonic(comm):
    frames = run_mission(comm, 400.0)
    values = [float(f[I_BATT]) for f in frames]
    for prev, curr in zip(values, values[1:], strict=False):
        assert curr <= prev, f"battery increased: {prev} -> {curr}"
    assert values[0] == 100.0


def test_battery_within_bounds(comm):
    frames = run_mission(comm, 400.0)
    for f in frames:
        batt = float(f[I_BATT])
        assert 0.0 <= batt <= 100.0


def test_battery_drops_over_mission(comm):
    frames = run_mission(comm, 300.0)
    assert float(frames[0][I_BATT]) > float(frames[-1][I_BATT])


def test_battery_drains_faster_during_burn(comm):
    # A 5-second stretch at burnout drains more than 5 seconds of coasting.
    idle_frames = run_mission(comm, 5.0, step=0.05, start=10.0)  # after burnout
    idle_drop = float(idle_frames[0][I_BATT]) - float(idle_frames[-1][I_BATT])
    burn_frames = run_mission(comm, 5.0, step=0.05, start=0.0)  # includes the burn
    burn_drop = float(burn_frames[0][I_BATT]) - float(burn_frames[-1][I_BATT])
    assert burn_drop > idle_drop


# --------------------------------------------------------------------------- #
# Real-time mission clock
# --------------------------------------------------------------------------- #
def test_dummy_time_tracks_wall_clock(comm):
    # The mission clock is monotonic-based (see communication.py), so it must
    # advance 1:1 with the internal clock. Fast-forward it deterministically
    # instead of sleeping: a real ``time.sleep`` is flaky on loaded CI runners,
    # where a descheduled process makes the wall clock run ahead of the sleep.
    frame0 = comm.getData()
    comm._dummy_start = time.monotonic() - 1.0
    frame1 = comm.getData()
    elapsed_ms = float(frame1[I_TIME]) - float(frame0[I_TIME])
    assert elapsed_ms == pytest.approx(1000.0, abs=50.0)


# --------------------------------------------------------------------------- #
# Serial frame validation
# --------------------------------------------------------------------------- #
def test_is_valid_frame_accepts_good_frame():
    good = ["0", "0", "0", "20", "1013", "0", "0", "0", "0", "0", "9.8"]
    assert Communication._is_valid_frame(good) is True


def test_is_valid_frame_rejects_empty_first_field():
    bad = ["", "0", "0", "20", "1013", "0", "0", "0", "0", "0", "9.8"]
    assert Communication._is_valid_frame(bad) is False


def test_is_valid_frame_rejects_non_numeric():
    bad = ["HELLO", "0", "0", "20", "1013", "0", "0", "0", "0", "0", "9.8"]
    assert Communication._is_valid_frame(bad) is False


def test_is_valid_frame_rejects_short_frame():
    short = ["0", "0", "0", "20", "1013"]
    assert Communication._is_valid_frame(short) is False


def test_is_valid_frame_rejects_empty():
    assert Communication._is_valid_frame([]) is False


def test_is_valid_frame_rejects_non_finite():
    # A single nan/inf sample would permanently corrupt the speed integrator
    # and could break plot auto-ranging, so the validator must drop it.
    for bad in ["nan", "inf", "-inf", "1e999"]:
        frame = [bad, "0", "0", "20", "1013", "0", "0", "0", "0", "0", "9.8"]
        assert Communication._is_valid_frame(frame) is False, bad


# --------------------------------------------------------------------------- #
# Extreme-altitude safety
# --------------------------------------------------------------------------- #
def test_pressure_finite_at_extreme_altitude(monkeypatch, comm):
    # The barometric formula used to produce a complex number above ~44 km,
    # which crashed round(); the clamped base must keep it finite instead.
    monkeypatch.setattr(
        comm,
        "_flight_state",
        lambda t: {"alt": 50000.0, "free_fall": 0, "accel_z": 9.81, "motor_on": False},
    )
    frame = comm.getData()
    assert math.isfinite(float(frame[I_PRESS]))
    assert float(frame[I_PRESS]) >= 0.0
