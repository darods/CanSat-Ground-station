import numpy as np
import pyqtgraph as pg


class graph_pressure(pg.PlotItem):
    """Plot item for displaying Barometric Pressure (hPa)."""

    def __init__(
        self,
        parent=None,
        name=None,
        labels=None,
        title="Barometric Pressure (hPa)",
        viewBox=None,
        axisItems=None,
        enableMenu=True,
        **kargs,
    ):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.pressure_plot = self.plot(pen=(102, 252, 241))
        self.pressure_data = np.zeros(30)
        self.ptr = 0

    def update(self, value):
        try:
            self.pressure_data[:-1] = self.pressure_data[1:]
            self.pressure_data[-1] = float(value)
            self.ptr += 1
            self.pressure_plot.setData(self.pressure_data)
            self.pressure_plot.setPos(self.ptr, 0)
        except (ValueError, TypeError):
            pass