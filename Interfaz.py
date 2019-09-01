from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from numpy import *
import serial

# Variables del puerto serial
portName = '/dev/ttyUSB0'
baudrate = 9600
ser = serial.Serial(portName, baudrate)

# Variables de la interfaz
app = QtGui.QApplication([])
view = pg.GraphicsView()
Grafico = pg.GraphicsLayout()
view.setCentralItem(Grafico)
view.show()
view.setWindowTitle('Monitereo de vuelo')
view.resize(800, 600)

# Fuente para mostrar solo un numero
font = QtGui.QFont()
font.setPixelSize(40)

# Title at top
text = """
Interfaz de monitroreo de vuelo para cansats y OBC's <br>
desarrollados en la Universidad Distrital.
"""
Grafico.addLabel(text, col=1, colspan=4)
Grafico.nextRow()

# Put vertical label on left side
Grafico.addLabel('RITA - Universidad Distrital', angle=-90, rowspan=3)


# Grafico de altitud
l1 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l1.setContentsMargins(10, 10, 10, 10)
l1.addLabel(
    "Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=3)
l1.nextRow()
p1 = l1.addPlot(title="Altura")
CurvaAltura = p1.plot()

# Graficos de tiempo, altura, caida y bateria
l2 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l2.setContentsMargins(10, 10, 10, 10)
l2.addLabel(
    "Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=2)
l2.nextRow()
p2 = l2.addPlot(title="Altura", rowspan=2)
textoAltura = pg.TextItem("test", anchor=(1, 1))
textoAltura.setFont(font)
p2.addItem(textoAltura)

vb = l2.addViewBox(lockAspect=True)
img = pg.ImageItem(np.random.normal(size=(100, 100)))
vb.addItem(img)
vb.autoRange()
l2.nextRow()
GrafBateria = l2.addPlot(title="bateria")

# Siguiente fila
Grafico.nextRow()

# Graficos de aceleraciones y angulos de euler
l3 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l3.setContentsMargins(10, 10, 10, 10)
l3.addLabel(
    "Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=3)
l3.nextRow()
l3.addLabel('Vertical Axis Label', angle=-90, rowspan=2)
p21 = l3.addPlot()
p22 = l3.addPlot()

# Graficos de valocidad, temperatura y presion
l4 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l4.setContentsMargins(10, 10, 10, 10)
l4.addLabel(
    "Sub-layout: this layout demonstrates the use of shared axes and axis labels", colspan=2)
l4.nextRow()
p4 = l4.addPlot(title="Plot 4", rowspan=2)
p5 = l4.addPlot(title="Plot 5")

l4.nextRow()
p6 = l4.addPlot()

# show some content in the plots
# p1.plot([1, 3, 2, 4, 3, 5])
p2.plot([1, 3, 2, 4, 3, 5])
p4.plot([1, 3, 2, 4, 3, 5])
p5.plot([1, 3, 2, 4, 3, 5])

Xa = linspace(0, 0)

# Realtime data plot. Each time this function is called,
# the data display is updated


def update():
    global curve, ptr, Xm
    # shift data in the temporal mean 1 sample left
    # Xm[:-1] = Xm[1:]
    Xa[:-1] = Xa[1:]
    # DatosAcelX[:-1] = DatosAcelX[1:]
    # DatosAcelY[:-1] = DatosAcelY[1:]
    # DatosAcelZ[:-1] = DatosAcelZ[1:]

    value = ser.readline()  # read line (single value) from the serial port
    decoded_bytes = str(value[0:len(value) - 2].decode("utf-8"))
    print(decoded_bytes)
    valor = decoded_bytes.split(",")
    # print(int(valor[0]))
    # vector containing the instantaneous values
    # Xm[-1] = int(valor[0])
    Xa[-1] = float(valor[1])
    '''
    DatosAcelX[-1] = float(valor[8])
    DatosAcelY[-1] = float(valor[9])
    DatosAcelZ[-1] = float(valor[10])
    '''
    # ptr += 1  # update x position for displaying the curve
    # curve.setData(Xm)                     # set the curve with this data
    # curve.setPos(ptr, 0)                   # set x position in the graph to 0

    CurvaAltura.setData(Xa)                     # set the curve with this data
    textoAltura.setText(str(valor[1]))
    '''
    curvaAcelX.setData(DatosAcelX)
    curvaAcelY.setData(DatosAcelY)
    curvaAcelZ.setData(DatosAcelZ)
    '''
    QtGui.QApplication.processEvents()    # you MUST process the plot now


Bandera = True
while Bandera:
    update()


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        Bandera = False
