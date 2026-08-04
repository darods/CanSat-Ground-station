import numpy as np
import pyqtgraph as pg


class graph_temperature(pg.PlotItem):
    """Plot item for displaying Temperature (°C)."""

    def __init__(
        self,
        parent=None,
        name=None,
        labels=None,
        title="Temperature (°C)",
        viewBox=None,
        axisItems=None,
        enableMenu=True,
        **kargs,
    ):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.temp_plot = self.plot(pen=(29, 185, 84))
        self.temp_data = np.zeros(30)
        self.ptr = 0

    def update(self, value):
        try:
            self.temp_data[:-1] = self.temp_data[1:]
            self.temp_data[-1] = float(value)
            self.ptr += 1
            self.temp_plot.setData(self.temp_data)
            self.temp_plot.setPos(self.ptr, 0)
        except (ValueError, TypeError):
            pass