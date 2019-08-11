from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

app = QtGui.QApplication([])
view = pg.GraphicsView()
l = pg.GraphicsLayout(border=(100, 100, 100))
view.setCentralItem(l)
view.show()
view.setWindowTitle('pyqtgraph example: GraphicsLayout')
view.resize(800, 600)

# Title at top
text = """
This puto example demonstrates the use of GraphicsLayout to arrange items in a grid.<br>
The items added to the layout must be subclasses of QGraphicsWidget (this includes <br>
PlotItem, ViewBox, LabelItem, and GrphicsLayout itself).
"""
l.addLabel(text, col=1, colspan=4)
l.nextRow()

# Put vertical label on left side
l.addLabel('RITA - Universidad Distrital', angle=-90, rowspan=3)

# Add 3 plots into the first row (automatic position)
l1 = l.addLayout(colspan=1, border=(50, 0, 0))
l1.setContentsMargins(10, 10, 10, 10)
l1.addLabel(
    "Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=3)
l1.nextRow()
p1 = l1.addPlot(title="Plot 1")

l2 = l.addLayout(colspan=1, border=(50, 0, 0))
l2.setContentsMargins(10, 10, 10, 10)
l2.addLabel(
    "Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=2)
l2.nextRow()
p2 = l2.addPlot(title="Plot 2", rowspan=2)
vb = l2.addViewBox(lockAspect=True)
img = pg.ImageItem(np.random.normal(size=(100, 100)))
vb.addItem(img)
vb.autoRange()
l2.nextRow()
p6 = l2.addPlot()

# Add a sub-layout into the second row (automatic position)
# The added item should avoid the first column, which is already filled
l.nextRow()
l3 = l.addLayout(colspan=1, border=(50, 0, 0))
l3.setContentsMargins(10, 10, 10, 10)
l3.addLabel(
    "Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=3)
l3.nextRow()
l3.addLabel('Vertical Axis Label', angle=-90, rowspan=2)
p21 = l3.addPlot()
p22 = l3.addPlot()


l4 = l.addLayout(colspan=1, border=(50, 0, 0))
l4.setContentsMargins(10, 10, 10, 10)
l4.addLabel(
    "Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=2)
l4.nextRow()
p4 = l4.addPlot(title="Plot 4", rowspan=2)
p5 = l4.addPlot(title="Plot 5")

l4.nextRow()
p6 = l4.addPlot()

# show some content in the plots
p1.plot([1, 3, 2, 4, 3, 5])
p2.plot([1, 3, 2, 4, 3, 5])
p4.plot([1, 3, 2, 4, 3, 5])
p5.plot([1, 3, 2, 4, 3, 5])


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
