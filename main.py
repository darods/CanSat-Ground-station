"""
Flight Monitoring Interface for CanSats and OBCs.
Supports Linux, macOS, and Windows 11 with PyQt6/PyQt5 and pyqtgraph.
"""

import sys
import argparse
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

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


def main():
    parser = argparse.ArgumentParser(description="CanSat Ground Station Flight Monitoring Interface")
    parser.add_argument("--port", type=str, default=None, help="Serial port (e.g. /dev/ttyUSB0, COM3, /dev/tty.usbmodem14101)")
    parser.add_argument("--baud", type=int, default=9600, help="Baud rate (default: 9600)")
    parser.add_argument("--dummy", action="store_true", help="Force simulated telemetry data mode")
    parser.add_argument("--interval", type=int, default=50, help="Telemetry update interval in ms (default: 50)")
    args = parser.parse_args()

    # PyQtGraph theme configuration
    pg.setConfigOption("background", (33, 33, 33))
    pg.setConfigOption("foreground", (197, 198, 199))

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
        try:
            value_chain = ser.getData()
            if not value_chain or len(value_chain) < 11:
                return
            altitude.update(value_chain[1])
            speed.update(value_chain[8], value_chain[9], value_chain[10])
            time_graph.update(value_chain[0])
            acceleration.update(value_chain[8], value_chain[9], value_chain[10])
            gyro.update(value_chain[5], value_chain[6], value_chain[7])
            pressure.update(value_chain[4])
            temperature.update(value_chain[3])
            free_fall.update(value_chain[2])
            db.guardar(value_chain)
        except IndexError:
            pass
        except Exception as e:
            print(f"[GroundStation] Update error: {e}")

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(args.interval)

    # Cross-version Qt execution
    exec_func = getattr(app, "exec", getattr(app, "exec_", None))
    sys.exit(exec_func())


if __name__ == "__main__":
    main()
