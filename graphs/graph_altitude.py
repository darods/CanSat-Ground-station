import pyqtgraph as pg
import numpy as np

class graph_altitude(pg.PlotItem):

    def __init__(self, parent=None, name=None, labels=None, title='Altitude (m)2', viewBox=None, axisItems=None, enableMenu=True, **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        self.altitude_plot = self.plot(pen=(29, 185, 84))
        self.altitude_data = np.linspace(0, 0, 30)
        self.ptr1 = 0

    def update(self, value):
        #self.altitude_plot, self.altitude_data,  self.ptr1
        self.altitude_data[:-1] = self.altitude_data[1:]
        self.altitude_data[-1] = float(value)
        self.ptr1 += 1
        self.altitude_plot.setData(self.altitude_data)
        self.altitude_plot.setPos(self.ptr1, 0)