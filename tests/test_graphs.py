"""
Unit tests for the graph panels (``graphs/``).

These pin down the behaviour developers touch most when adding or changing a
panel:

* ``ScrollingPlot`` -- the ring buffer scrolls, freezes while the user drags
  the panel and resumes afterwards, and bad samples never crash it.
* ``TextPlot`` -- the readouts stay centered in the view and therefore never
  vanish after auto-range or pan/zoom (the old issue #4).
* Each concrete graph maps telemetry fields to its ``update()`` correctly.

No panel is shown on screen; everything runs headless via the root
``conftest.py``.
"""

import time

import numpy as np

from graphs.base import ScrollingPlot, ScrollingViewBox, TextPlot


# --------------------------------------------------------------------------- #
# ScrollingPlot: ring buffer
# --------------------------------------------------------------------------- #
def test_push_advances_pointer(qtbot, altitude_graph):
    altitude_graph.update("10")
    altitude_graph.update("20")
    assert altitude_graph.ptr == 2


def test_push_stores_last_samples(qtbot, altitude_graph):
    for i in range(10):
        altitude_graph.update(str(i))
    _, y = altitude_graph._curves[0].getData()
    assert y[-1] == 9.0
    assert y[-2] == 8.0
    assert len(y) == 300  # the visible ring-buffer window


def test_curve_follows_pointer(qtbot, altitude_graph):
    altitude_graph.update("5")
    assert altitude_graph._curves[0].pos().x() == 1


def test_multiline_plot_stores_each_trace(qtbot, acceleration_graph):
    acceleration_graph.update("1", "2", "3")
    acceleration_graph.update("4", "5", "6")
    for i, curve in enumerate(acceleration_graph._curves):
        _, y = curve.getData()
        assert y[-1] == float([4, 5, 6][i])
    assert len(acceleration_graph._curves) == 3


def test_bad_value_is_ignored(qtbot, altitude_graph):
    altitude_graph.update("not-a-number")  # must not raise
    assert altitude_graph.ptr == 0


# --------------------------------------------------------------------------- #
# ScrollingPlot: drag-pause behaviour (the "line runs away" fix)
# --------------------------------------------------------------------------- #
def test_push_skipped_while_paused(qtbot, altitude_graph):
    altitude_graph.update("10")
    altitude_graph.vb.live_paused = True
    altitude_graph.update("20")  # user is dragging the panel
    assert altitude_graph.ptr == 1
    assert altitude_graph._curves[0].pos().x() == 1


def test_push_resumes_after_release(qtbot, altitude_graph):
    altitude_graph.vb.live_paused = True
    altitude_graph.update("1")
    assert altitude_graph.ptr == 0
    altitude_graph.vb.live_paused = False
    altitude_graph.update("2")
    assert altitude_graph.ptr == 1


def test_viewbox_toggles_pause_on_drag(qtbot):
    vb = ScrollingViewBox()
    assert vb.live_paused is False
    vb.live_paused = True
    assert vb.live_paused is True


# --------------------------------------------------------------------------- #
# TextPlot: readouts that never vanish
# --------------------------------------------------------------------------- #
def _is_centered(plot) -> bool:
    px, py = plot.text_item.pos().x(), plot.text_item.pos().y()
    (xr, yr) = plot.viewRange()
    return (
        abs(px - (xr[0] + xr[1]) / 2.0) < 1e-6
        and abs(py - (yr[0] + yr[1]) / 2.0) < 1e-6
    )


def test_text_plot_starts_centered(qtbot, time_graph):
    assert _is_centered(time_graph)


def test_text_plot_recenters_after_autorange(qtbot, time_graph):
    time_graph.getViewBox().autoRange()  # used to make the text vanish
    assert _is_centered(time_graph)


def test_text_plot_recenters_after_pan_zoom(qtbot, time_graph):
    time_graph.setRange(xRange=(-1000, 3000), yRange=(-500, 500), padding=0)
    assert _is_centered(time_graph)


def test_time_readout(qtbot, time_graph):
    time_graph.update("120000")  # ms
    assert time_graph.text_item.toPlainText() == "2.00"


def test_time_readout_ignores_bad_value(qtbot, time_graph):
    time_graph.update("nope")  # must not raise or change the readout
    assert time_graph.text_item.toPlainText() == "0.0"


def test_free_fall_readout(qtbot, free_fall_graph):
    free_fall_graph.update("1")
    assert free_fall_graph.text_item.toPlainText() == "Yes"
    free_fall_graph.update("0")
    assert free_fall_graph.text_item.toPlainText() == "No"


def test_battery_readout(qtbot, battery_graph):
    battery_graph.update("87.4")
    assert battery_graph.text_item.toPlainText() == "87%"


def test_battery_readout_keeps_last_value_when_absent(qtbot, battery_graph):
    battery_graph.update("99")
    battery_graph.update(None)  # no battery field in the frame
    assert battery_graph.text_item.toPlainText() == "99%"


# --------------------------------------------------------------------------- #
# Specific graphs
# --------------------------------------------------------------------------- #
def test_gyro_update(qtbot, gyro_graph):
    gyro_graph.update("-1.5", "2.5", "0")
    assert gyro_graph.ptr == 1


def test_pressure_and_temperature_update(qtbot, pressure_graph, temperature_graph):
    pressure_graph.update("1013.25")
    temperature_graph.update("21.5")
    assert pressure_graph.ptr == 1
    assert temperature_graph.ptr == 1


def test_speed_integrates_acceleration(qtbot, speed_graph):
    speed_graph.update("0", "0", "9.81")  # baseline
    # Force a 1 s time step so the integration is deterministic.
    speed_graph._last_t = time.monotonic() - 1.0
    speed_graph.update("0", "0", "0")  # free fall: z accelerates down
    assert speed_graph.ptr == 2
    assert speed_graph.vz < 0.0
    assert speed_graph._curves[0].getData()[1][-1] > 0.0


def test_speed_ignores_bad_sample(qtbot, speed_graph):
    speed_graph.update("x", "y", "z")  # must not raise
    assert speed_graph.ptr == 0
