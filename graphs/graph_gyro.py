import numpy as np
import pyqtgraph as pg


class graph_gyro(pg.PlotItem):
    """Plot item for 3-axis Gyroscope data (Pitch, Roll, Yaw)."""

    def __init__(
        self,
        parent=None,
        name=None,
        labels=None,
        title="Gyroscope (°/s)",
        viewBox=None,
        axisItems=None,
        enableMenu=True,
        **kargs,
    ):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.hideAxis("bottom")
        self.addLegend()

        self.pitch_plot = self.plot(pen=(102, 252, 241), name="Pitch")
        self.roll_plot = self.plot(pen=(29, 185, 84), name="Roll")
        self.yaw_plot = self.plot(pen=(203, 45, 111), name="Yaw")

        self.pitch_data = np.zeros(30)
        self.roll_data = np.zeros(30)
        self.yaw_data = np.zeros(30)
        self.ptr = 0

    def update(self, pitch, roll, yaw):
        try:
            self.pitch_data[:-1] = self.pitch_data[1:]
            self.roll_data[:-1] = self.roll_data[1:]
            self.yaw_data[:-1] = self.yaw_data[1:]

            self.pitch_data[-1] = float(pitch)
            self.roll_data[-1] = float(roll)
            self.yaw_data[-1] = float(yaw)

            self.ptr += 1

            self.pitch_plot.setData(self.pitch_data)
            self.roll_plot.setData(self.roll_data)
            self.yaw_plot.setData(self.yaw_data)

            self.pitch_plot.setPos(self.ptr, 0)
            self.roll_plot.setPos(self.ptr, 0)
            self.yaw_plot.setPos(self.ptr, 0)
        except (ValueError, TypeError):
            pass