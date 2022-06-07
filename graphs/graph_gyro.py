import pyqtgraph as pg
import numpy as np

class graph_gyro(pg.PlotItem):
    
    def __init__(self, parent=None, name=None, labels=None, title='Gyro', viewBox=None, axisItems=None, enableMenu=True, **kargs):
        super().__init__(parent, name, labels, title, viewBox, axisItems, enableMenu, **kargs)

        self.hideAxis('bottom')
        # adding legend
        self.addLegend()
        self.pitch_plot = self.plot(pen=(102, 252, 241), name="Pitch")
        self.roll_plot = self.plot(pen=(29, 185, 84), name="Roll")
        self.yaw_plot = self.plot(pen=(203, 45, 111), name="Yaw")

        self.pitch_data = np.linspace(0, 0)
        self.roll_data = np.linspace(0, 0)
        self.yaw_data = np.linspace(0, 0)
        self.ptr = 0


    def update(self, pitch, roll, yaw):

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