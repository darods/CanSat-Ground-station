"""
Flight Monitoring Interface for CanSats and OBCs.
Supports Linux, macOS, and Windows 11 with PyQt6/PyQt5 and pyqtgraph.
"""

import argparse
import sys

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from communication import Communication
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

# Minimum fields a usable telemetry frame must carry (the 12th, battery,
# is optional and only sent in dummy mode).
MIN_FRAME_FIELDS = 11


def dispatch_frame(
    frame,
    altitude,
    speed,
    acceleration,
    gyro,
    pressure,
    temperature,
    time_graph,
    free_fall,
    battery,
    db=None,
):
    """Dispatch one parsed telemetry frame to every graph panel.

    The frame follows the comma-separated schema documented in ``README.md``:

    * ``frame[0]``  elapsed time (ms) -> ``time_graph``
    * ``frame[1]``  altitude (m)     -> ``altitude``
    * ``frame[2]``  free-fall flag   -> ``free_fall``
    * ``frame[3]``  temperature (°C) -> ``temperature``
    * ``frame[4]``  pressure (hPa)   -> ``pressure``
    * ``frame[5..7]``  gyro pitch/roll/yaw -> ``gyro``
    * ``frame[8..10]`` accel X/Y/Z   -> ``acceleration`` and ``speed``
    * ``frame[11]`` battery (%)      -> ``battery`` (optional; older hardware
      frames may omit it and the readout simply keeps its last value)

    If ``db`` is given the frame is also persisted. Returns ``True`` when the
    frame was processed, ``False`` when it was too short to use.
    """
    if not frame or len(frame) < MIN_FRAME_FIELDS:
        return False
    altitude.update(frame[1])
    speed.update(frame[8], frame[9], frame[10])
    time_graph.update(frame[0])
    acceleration.update(frame[8], frame[9], frame[10])
    gyro.update(frame[5], frame[6], frame[7])
    pressure.update(frame[4])
    temperature.update(frame[3])
    free_fall.update(frame[2])
    if len(frame) > MIN_FRAME_FIELDS:
        battery.update(frame[MIN_FRAME_FIELDS])
    if db is not None:
        db.guardar(frame)
    return True


def main():  # pragma: no cover - GUI entry point, not unit-tested
    parser = argparse.ArgumentParser(
        description="CanSat Ground Station Flight Monitoring Interface"
    )
    parser.add_argument(
        "--port",
        type=str,
        default=None,
        help="Serial port (e.g. /dev/ttyUSB0, COM3, /dev/tty.usbmodem14101)",
    )
    parser.add_argument(
        "--baud", type=int, default=9600, help="Baud rate (default: 9600)"
    )
    parser.add_argument(
        "--dummy", action="store_true", help="Force simulated telemetry data mode"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=50,
        help="Telemetry update interval in ms (default: 50)",
    )
    args = parser.parse_args()
    # A polling interval of 0 or less would make the timer fire as fast as
    # possible and starve the event loop; enforce a sane floor.
    args.interval = max(10, args.interval)

    # PyQtGraph theme configuration
    pg.setConfigOption("background", (33, 33, 33))
    pg.setConfigOption("foreground", (197, 198, 199))
    pg.setConfigOptions(antialias=True)

    # Initialize Qt Application
    app = QtWidgets.QApplication(sys.argv)
    view = pg.GraphicsView()
    layout = pg.GraphicsLayout()
    view.setCentralItem(layout)
    view.setWindowTitle("CanSat Flight Monitoring Station")
    view.resize(1200, 700)

    # Initialize Communication & Data Storage
    ser = Communication(port=args.port, baudrate=args.baud, force_dummy=args.dummy)
    db = DataBase()

    # Font setup
    font = QtGui.QFont()
    font.setPixelSize(90)

    # Widget styles
    button_style = "background-color: rgb(29, 185, 84); color: rgb(0,0,0); font-size: 14px; font-weight: bold; border-radius: 4px; padding: 6px;"

    # Controls Setup
    proxy_start = QtWidgets.QGraphicsProxyWidget()
    save_button = QtWidgets.QPushButton("Start storage")
    save_button.setStyleSheet(button_style)
    save_button.clicked.connect(db.start)
    proxy_start.setWidget(save_button)

    proxy_stop = QtWidgets.QGraphicsProxyWidget()
    end_save_button = QtWidgets.QPushButton("Stop storage")
    end_save_button.setStyleSheet(button_style)
    end_save_button.clicked.connect(db.stop)
    proxy_stop.setWidget(end_save_button)

    # Graph Instances
    altitude = graph_altitude()
    speed = graph_speed()
    acceleration = graph_acceleration()
    gyro = graph_gyro()
    pressure = graph_pressure()
    temperature = graph_temperature()
    time_graph = graph_time(font=font)
    battery = graph_battery(font=font)
    free_fall = graph_free_fall(font=font)

    # Layout Assembly
    header_text = (
        "Flight monitoring interface for CanSats and OBCs<br>"
        "Developed at Universidad Distrital FJC | Modernized for Linux, macOS & Windows 11"
    )
    layout.addLabel(header_text, col=1, colspan=21)
    layout.nextRow()

    layout.addLabel("LIDER - ATL research hotbed", angle=-90, rowspan=3)
    layout.nextRow()

    btn_layout = layout.addLayout(colspan=21)
    btn_layout.addItem(proxy_start)
    btn_layout.nextCol()
    btn_layout.addItem(proxy_stop)
    layout.nextRow()

    left_layout = layout.addLayout(colspan=20, rowspan=2)
    top_row = left_layout.addLayout(rowspan=1, border=(83, 83, 83))
    top_row.addItem(altitude)
    top_row.addItem(speed)
    left_layout.nextRow()

    mid_row = left_layout.addLayout(rowspan=1, border=(83, 83, 83))
    mid_row.addItem(acceleration)
    mid_row.addItem(gyro)
    mid_row.addItem(pressure)
    mid_row.addItem(temperature)

    right_layout = layout.addLayout(border=(83, 83, 83))
    right_layout.addItem(time_graph)
    right_layout.nextRow()
    right_layout.addItem(battery)
    right_layout.nextRow()
    right_layout.addItem(free_fall)

    view.show()

    def update():
        """Poll one telemetry frame and feed every panel with its fields."""
        dispatch_frame(
            ser.getData(),
            altitude,
            speed,
            acceleration,
            gyro,
            pressure,
            temperature,
            time_graph,
            free_fall,
            battery,
            db=db,
        )

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(args.interval)

    # Cross-version Qt execution
    exec_func = getattr(app, "exec", getattr(app, "exec_", None))
    sys.exit(exec_func())


if __name__ == "__main__":  # pragma: no cover
    main()
