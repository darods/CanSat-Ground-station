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
font.setPixelSize(120)
font2 = QtGui.QFont()
font2.setPixelSize(90)


# Title at top
text = """
Interfaz de monitroreo de vuelo para cansats y OBC's <br>
desarrollados en la Universidad Distrital.
"""
Grafico.addLabel(text, col=1, colspan=4)
Grafico.nextRow()

# Put vertical label on left side
Grafico.addLabel('LIDER - Universidad Distrital', angle=-90, rowspan=3)


# Grafico de altitud
l1 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l1.setContentsMargins(10, 10, 10, 10)
p1 = l1.addPlot(title="Altura")
p1.hideAxis('bottom')
CurvaAltura = p1.plot()

# Graficos de tiempo, altura, caida y bateria
l2 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l2.setContentsMargins(10, 10, 10, 10)

GrafAltura = l2.addPlot(title="Altura", rowspan=2)
GrafAltura.hideAxis('bottom')
GrafAltura.hideAxis('left')
textoAltura = pg.TextItem("test", anchor=(0.5, 0.5))
textoAltura.setFont(font)
GrafAltura.addItem(textoAltura)
# Grafico del tiempo
GrafTiempo = l2.addPlot(title="Tiempo")
GrafTiempo.hideAxis('bottom')
GrafTiempo.hideAxis('left')
textoTiempo = pg.TextItem("test", anchor=(0.5, 0.5))
textoTiempo.setFont(font2)
GrafTiempo.addItem(textoTiempo)
l2.nextRow()
# Grafico de la batería
GrafBateria = l2.addPlot(title="bateria")
GrafBateria.hideAxis('bottom')
GrafBateria.hideAxis('left')
textoBateria = pg.TextItem("test", anchor=(0.5, 0.5))
textoBateria.setFont(font2)
GrafBateria.addItem(textoBateria)

# Siguiente fila
Grafico.nextRow()

# Graficos de aceleraciones y angulos de euler
l3 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l3.setContentsMargins(10, 10, 10, 10)

l3.addLabel('Vertical Axis Label', angle=-90, rowspan=2)
GrafAcel = l3.addPlot(title="Aceleraciones")
# añadiendo leyenda
GrafAcel.addLegend()
GrafAcel.hideAxis('bottom')
curvaAcelX = GrafAcel.plot(pen="r", name="AcelX")
curvaAcelY = GrafAcel.plot(pen="g", name="AcelY")
curvaAcelZ = GrafAcel.plot(pen="b", name="AcelX")

GrafEuler = l3.addPlot(title="Angulos Euler")
GrafEuler.hideAxis('bottom')
# añadiendo leyenda
GrafEuler.addLegend()
curvaPitch = GrafEuler.plot(pen="r", name="Pitch")
curvaRoll = GrafEuler.plot(pen="g", name="Roll")
curvaYaw = GrafEuler.plot(pen="b", name="Yaw")

# Graficos de valocidad, temperatura y presion
l4 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l4.setContentsMargins(10, 10, 10, 10)

GrafVel = l4.addPlot(title="Velocidad", rowspan=2)
GrafVel.hideAxis('bottom')
GrafVel.hideAxis('left')
textoVel = pg.TextItem("test", anchor=(0.5, 0.5))
textoVel.setFont(font)
GrafVel.addItem(textoVel)

GrafTemp = l4.addPlot(title="Temperatura")
GrafTemp.hideAxis('bottom')
GrafTemp.hideAxis('left')
textoTemp = pg.TextItem("test", anchor=(0.5, 0.5))
textoTemp.setFont(font2)
GrafTemp.addItem(textoTemp)

l4.nextRow()
GrafPress = l4.addPlot(title="Presion")
GrafPress.hideAxis('bottom')
GrafPress.hideAxis('left')
textoPress = pg.TextItem("test", anchor=(0.5, 0.5))
textoPress.setFont(font2)
GrafPress.addItem(textoPress)

# show some content in the plots
# p1.plot([1, 3, 2, 4, 3, 5])
# GrafAltura.plot([1, 3, 2, 4, 3, 5])

# Creando los arreglos que guardan los puntos de los graficos
Xa = linspace(0, 0)
DatosAcelX = linspace(0, 0)
DatosAcelY = linspace(0, 0)
DatosAcelZ = linspace(0, 0)

DatosPitch = linspace(0, 0)
DatosRoll = linspace(0, 0)
DatosYaw = linspace(0, 0)
# Realtime data plot. Each time this function is called,
# the data display is updated


def update():
    global curve, ptr, Xm
    # shift data in the temporal mean 1 sample left
    # Xm[:-1] = Xm[1:]
    Xa[:-1] = Xa[1:]
    DatosAcelX[:-1] = DatosAcelX[1:]
    DatosAcelY[:-1] = DatosAcelY[1:]
    DatosAcelZ[:-1] = DatosAcelZ[1:]
    DatosPitch[:-1] = DatosPitch[1:]
    DatosRoll[:-1] = DatosRoll[1:]
    DatosYaw[:-1] = DatosYaw[1:]

    value = ser.readline()  # read line (single value) from the serial port
    decoded_bytes = str(value[0:len(value) - 2].decode("utf-8"))
    print(decoded_bytes)
    valor = decoded_bytes.split(",")
    # print(int(valor[0]))
    # vector containing the instantaneous values
    # Xm[-1] = int(valor[0])
    Xa[-1] = float(valor[1])

    DatosAcelX[-1] = float(valor[8])
    DatosAcelY[-1] = float(valor[9])
    DatosAcelZ[-1] = float(valor[10])

    DatosPitch[-1] = float(valor[5])
    DatosRoll[-1] = float(valor[6])
    DatosYaw[-1] = float(valor[7])

    # ptr += 1  # update x position for displaying the curve
    # curve.setData(Xm)                     # set the curve with this data
    # curve.setPos(ptr, 0)                   # set x position in the graph to 0

    CurvaAltura.setData(Xa)                     # set the curve with this data
    textoAltura.setText(str(valor[1]))

    curvaAcelX.setData(DatosAcelX)
    curvaAcelY.setData(DatosAcelY)
    curvaAcelZ.setData(DatosAcelZ)

    curvaPitch.setData(DatosPitch)
    curvaRoll.setData(DatosRoll)
    curvaYaw.setData(DatosYaw)

    textoTemp.setText(str(valor[3]))
    textoPress.setText(str(valor[4]))

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
