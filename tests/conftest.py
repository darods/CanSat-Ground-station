"""
Pytest fixtures shared by the graph and dispatch tests.

Anything that builds a pyqtgraph widget needs a running ``QApplication``.
pytest-qt's ``qtbot`` fixture provides one implicitly (headless via the root
``conftest.py``). Graph panels do not need to be shown on screen to be
tested, so these fixtures simply construct each panel::

    def test_something(qtbot, altitude_graph):
        altitude_graph.update("123.4")
        assert altitude_graph.ptr == 1
"""

import pytest

from graphs.graph_acceleration import graph_acceleration
from graphs.graph_altitude import graph_altitude
from graphs.graph_battery import graph_battery
from graphs.graph_free_fall import graph_free_fall
from graphs.graph_gyro import graph_gyro
from graphs.graph_pressure import graph_pressure
from graphs.graph_speed import graph_speed
from graphs.graph_temperature import graph_temperature
from graphs.graph_time import graph_time


@pytest.fixture
def altitude_graph(qtbot):
    return graph_altitude()


@pytest.fixture
def speed_graph(qtbot):
    return graph_speed()


@pytest.fixture
def acceleration_graph(qtbot):
    return graph_acceleration()


@pytest.fixture
def gyro_graph(qtbot):
    return graph_gyro()


@pytest.fixture
def pressure_graph(qtbot):
    return graph_pressure()


@pytest.fixture
def temperature_graph(qtbot):
    return graph_temperature()


@pytest.fixture
def time_graph(qtbot):
    return graph_time()


@pytest.fixture
def battery_graph(qtbot):
    return graph_battery()


@pytest.fixture
def free_fall_graph(qtbot):
    return graph_free_fall()
