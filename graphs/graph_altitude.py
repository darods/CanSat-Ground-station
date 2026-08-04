import numpy as np
import pyqtgraph as pg


class graph_altitude(pg.PlotItem):
    """Plot item for displaying Altitude (m)."""

    def __init__(
        self,
        parent=None,
        name=None,
        labels=None,
        title="Altitude (m)",
        viewBox=None,
        axisItems=None,
        enableMenu=True,
        **kargs,
    ):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.altitude_plot = self.plot(pen=(29, 185, 84))
        self.altitude_data = np.zeros(30)
        self.ptr1 = 0

    def update(self, value):
        try:
            self.altitude_data[:-1] = self.altitude_data[1:]
            self.altitude_data[-1] = float(value)
            self.ptr1 += 1
            self.altitude_plot.setData(self.altitude_data)
            self.altitude_plot.setPos(self.ptr1, 0)
        except (ValueError, TypeError):
            pass