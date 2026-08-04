import math
import numpy as np
import pyqtgraph as pg


class graph_speed(pg.PlotItem):
    """Plot item for displaying magnitude speed (m/s)."""

    def __init__(
        self,
        parent=None,
        name=None,
        labels=None,
        title="Speed (m/s)",
        viewBox=None,
        axisItems=None,
        enableMenu=True,
        **kargs,
    ):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.vel_plot = self.plot(pen=(29, 185, 84))
        self.vel_data = np.zeros(30)
        self.ptr = 0
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.vzo = None

    def update(self, vx, vy, vz):
        try:
            ax = float(vx)
            ay = float(vy)
            az = float(vz)

            if self.vzo is None:
                self.vzo = az

            dt = 0.5  # 500 ms in seconds
            self.vx += ax * dt
            self.vy += ay * dt
            self.vz += (az - self.vzo) * dt

            vel_sq = math.pow(self.vx, 2) + math.pow(self.vy, 2) + math.pow(self.vz, 2)
            vel = math.sqrt(vel_sq)

            self.vel_data[:-1] = self.vel_data[1:]
            self.vel_data[-1] = vel
            self.ptr += 1
            self.vel_plot.setData(self.vel_data)
            self.vel_plot.setPos(self.ptr, 0)
        except (ValueError, TypeError):
            pass