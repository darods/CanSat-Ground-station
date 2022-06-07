import pyqtgraph as pg
import numpy as np

class graph_acceleration(pg.PlotItem):
     
    def __init__(self, parent=None, name=None, labels=None, title='Accelerations (m/s²)', viewBox=None, axisItems=None, enableMenu=True, **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)
        
        self.addLegend()
        self.hideAxis('bottom')

        self.accX_plot = self.plot(pen=(102, 252, 241), name="X")
        self.accY_plot = self.plot(pen=(29, 185, 84), name="Y")
        self.accZ_plot = self.plot(pen=(203, 45, 111), name="Z")

        self.accX_data = np.linspace(0, 0)
        self.accY_data = np.linspace(0, 0)
        self.accZ_data = np.linspace(0, 0)
        self.ptr = 0


    def update(self, ax, ay, az):

        self.accX_data[:-1] = self.accX_data[1:]
        self.accY_data[:-1] = self.accY_data[1:]
        self.accZ_data[:-1] = self.accZ_data[1:]

        self.accX_data[-1] = float(ax)
        self.accY_data[-1] = float(ay)
        self.accZ_data[-1] = float(az)
        self.ptr += 1

        self.accX_plot.setData(self.accX_data)
        self.accY_plot.setData(self.accY_data)
        self.accZ_plot.setData(self.accZ_data)

        self.accX_plot.setPos(self.ptr, 0)
        self.accY_plot.setPos(self.ptr, 0)
        self.accZ_plot.setPos(self.ptr, 0)