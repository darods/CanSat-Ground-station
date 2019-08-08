from PyQt5 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
# Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

# Define a top-level widget to hold everything
w = QtGui.QWidget()

# Create some widgets to be placed inside
btn = QtGui.QPushButton('press me')
text = QtGui.QLineEdit('enter text')
listw = QtGui.QListWidget()
plot = pg.PlotWidget(name='plot 1')
plot2 = pg.PlotWidget(name='plot 2')
plot3 = pg.PlotWidget(name='plot 3')
plot4 = pg.PlotWidget(name='plot 3')

curve = plot4.plot(pen='r')
data = np.random.normal(size=(10, 1000))
ptr = 0


def update():
    global curve, data, ptr, p6
    curve.setData(data[ptr % 10])
    if ptr == 0:
        # stop auto-scaling after the first data set is plotted
        plot4.enableAutoRange('xy', False)
    ptr += 1


timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


plot.setLabel('left', 'Value', units='V')

# Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

# Add widgets to the layout in their proper positions
layout.addWidget(btn, 0, 0)   # button goes in upper-left
layout.addWidget(text, 1, 0)   # text edit goes in middle-left
layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
layout.addWidget(plot, 0, 1)  # plot goes on right side, spanning 3 rows
layout.addWidget(plot2, 0, 3)  # plot goes on right side, spanning 3 rows
layout.addWidget(plot3, 2, 1)  # plot goes on right side, spanning 3 rows
layout.addWidget(plot4, 2, 3)  # plot goes on right side, spanning 3 rows


# Display the widget as a new window
w.show()

# Start the Qt event loop
app.exec_()
