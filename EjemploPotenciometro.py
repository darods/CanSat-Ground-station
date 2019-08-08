# tomado de https://stackoverflow.com/questions/45046239/python-realtime-plot-using-pyqtgraph
# Import libraries
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import serial

# Create object serial port
portName = '/dev/ttyUSB0'                     # replace this port name by yours!
baudrate = 9600
ser = serial.Serial(portName, baudrate)

### START QtApp #####
# you MUST do this once (initialize things)
app = QtGui.QApplication([])
####################

win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window
# creates empty space for the plot in the window
p = win.addPlot(title="Realtime plot")
curve = p.plot()                     # create an empty "plot" (a curve to plot)

windowWidth = 500                    # width of the window displaying the curve
# create array that will contain the relevant time series
Xm = linspace(0, 0, windowWidth)
ptr = -windowWidth                      # set first x position

# Realtime data plot. Each time this function is called, the data display is updated


def update():
    global curve, ptr, Xm
    # shift data in the temporal mean 1 sample left
    Xm[:-1] = Xm[1:]
    value = ser.readline()                # read line (single value) from the serial port
    # vector containing the instantaneous values
    Xm[-1] = float(value)
    ptr += 1                              # update x position for displaying the curve
    curve.setData(Xm)                     # set the curve with this data
    curve.setPos(ptr, 0)                   # set x position in the graph to 0
    QtGui.QApplication.processEvents()    # you MUST process the plot now


### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot
while True:
    update()

### END QtApp ####
app.exec_()  # you MUST put this at the end
##################
