"""
Unit tests for the frame dispatch logic (``main.dispatch_frame``).

``dispatch_frame`` is the function that maps one parsed telemetry frame onto
every graph panel. It was extracted from the GUI update loop specifically so
the frame schema can be validated without launching the application. Keep
these tests in sync whenever the telemetry schema in ``README.md`` changes.
"""

from dataBase import DataBase
from graphs.graph_acceleration import graph_acceleration
from graphs.graph_altitude import graph_altitude
from graphs.graph_battery import graph_battery
from graphs.graph_free_fall import graph_free_fall
from graphs.graph_gyro import graph_gyro
from graphs.graph_pressure import graph_pressure
from graphs.graph_speed import graph_speed
from graphs.graph_temperature import graph_temperature
from graphs.graph_time import graph_time
from main import dispatch_frame


def build_panel():
    """Construct one of every graph panel (requires a QApplication)."""
    return {
        "altitude": graph_altitude(),
        "speed": graph_speed(),
        "acceleration": graph_acceleration(),
        "gyro": graph_gyro(),
        "pressure": graph_pressure(),
        "temperature": graph_temperature(),
        "time": graph_time(),
        "battery": graph_battery(),
        "free_fall": graph_free_fall(),
    }


def full_frame():
    """A complete 12-field dummy frame (including the optional battery)."""
    return [
        "60000",
        "123.4",
        "1",
        "21.5",
        "900.1",
        "1.1",
        "2.2",
        "3.3",
        "0.1",
        "0.2",
        "9.8",
        "98.0",
    ]


def test_dispatch_feeds_every_panel(qtbot):
    p = build_panel()
    ok = dispatch_frame(
        full_frame(),
        p["altitude"],
        p["speed"],
        p["acceleration"],
        p["gyro"],
        p["pressure"],
        p["temperature"],
        p["time"],
        p["free_fall"],
        p["battery"],
    )
    assert ok is True
    assert p["altitude"].ptr == 1
    assert p["speed"].ptr == 1
    assert p["acceleration"].ptr == 1
    assert p["gyro"].ptr == 1
    assert p["pressure"].ptr == 1
    assert p["temperature"].ptr == 1
    assert p["time"].text_item.toPlainText() == "1.00"  # 60000 ms -> 1 min
    assert p["free_fall"].text_item.toPlainText() == "Yes"
    assert p["battery"].text_item.toPlainText() == "98%"


def test_dispatch_without_battery_field_keeps_readout(qtbot):
    p = build_panel()
    frame = full_frame()[:11]  # older hardware frame without battery
    dispatch_frame(
        frame,
        p["altitude"],
        p["speed"],
        p["acceleration"],
        p["gyro"],
        p["pressure"],
        p["temperature"],
        p["time"],
        p["free_fall"],
        p["battery"],
    )
    assert p["battery"].text_item.toPlainText() == "100%"  # unchanged default


def test_dispatch_rejects_short_frame(qtbot):
    p = build_panel()
    ok = dispatch_frame(
        ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        p["altitude"],
        p["speed"],
        p["acceleration"],
        p["gyro"],
        p["pressure"],
        p["temperature"],
        p["time"],
        p["free_fall"],
        p["battery"],
    )
    assert ok is False
    assert p["altitude"].ptr == 0


def test_dispatch_rejects_empty_frame(qtbot):
    p = build_panel()
    ok = dispatch_frame(
        [],
        p["altitude"],
        p["speed"],
        p["acceleration"],
        p["gyro"],
        p["pressure"],
        p["temperature"],
        p["time"],
        p["free_fall"],
        p["battery"],
    )
    assert ok is False
    assert p["time"].text_item.toPlainText() == "0.0"


def test_dispatch_persists_frame_when_db_given(qtbot, tmp_path):
    p = build_panel()
    db = DataBase(filename=tmp_path / "flight.csv")
    db.start()
    dispatch_frame(
        full_frame(),
        p["altitude"],
        p["speed"],
        p["acceleration"],
        p["gyro"],
        p["pressure"],
        p["temperature"],
        p["time"],
        p["free_fall"],
        p["battery"],
        db=db,
    )
    assert (tmp_path / "flight.csv").exists()
