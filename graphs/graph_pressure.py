import pyqtgraph as pg
import numpy as np


class graph_pressure(pg.PlotItem):
    
    def __init__(self, parent=None, name=None, labels=None, title='Barometric pressure', viewBox=None, axisItems=None, enableMenu=True, **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.pressure_plot = self.plot(pen=(102, 252, 241))
        self.pressure_data = np.linspace(0, 0, 30)
        self.ptr = 0


    def update(self, value):
        self.pressure_data[:-1] = self.pressure_data[1:]
        self.pressure_data[-1] = float(value)
        self.ptr += 1
        self.pressure_plot.setData(self.pressure_data)
        self.pressure_plot.setPos(self.ptr, 0)