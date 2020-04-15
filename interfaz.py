from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from comunicacion import Comunicacion


pg.setConfigOption('background', (227, 229, 219))
pg.setConfigOption('foreground', 'k')
# Variables de la interfaz
app = QtGui.QApplication([])
view = pg.GraphicsView()
Grafico = pg.GraphicsLayout()
view.setCentralItem(Grafico)
view.show()
view.setWindowTitle('Monitereo de vuelo')
view.resize(800, 600)

ser = Comunicacion()

# Fuente para mostrar solo un numero
font = QtGui.QFont('Arial', 120)

font2 = QtGui.QFont('Arial', 90)


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
# p1.hideAxis('bottom')
curva_altura = p1.plot(pen="r")
datos_altura = np.linspace(0, 0, 30)
ptr1 = 0


# Graficos de tiempo, altura, caida y bateria
l2 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l2.setContentsMargins(10, 10, 10, 10)

GrafAltura = l2.addPlot(title="Altura", rowspan=2)
GrafAltura.hideAxis('bottom')
GrafAltura.hideAxis('left')
textoAltura = pg.TextItem("test", anchor=(0.5, 0.5), color="k")
textoAltura.setFont(font)
GrafAltura.addItem(textoAltura)


def update_altura(valor):
    global curva_altura, datos_altura,  ptr1
    datos_altura[:-1] = datos_altura[1:]
    #valor = ser.getData()
    datos_altura[-1] = float(valor[1])
    ptr1 += 1
    curva_altura.setData(datos_altura)
    curva_altura.setPos(ptr1, 0)
    textoAltura.setText('')
    textoAltura.setText(str(ptr1))


# Grafico del tiempo
GrafTiempo = l2.addPlot(title="Tiempo")
GrafTiempo.hideAxis('bottom')
GrafTiempo.hideAxis('left')
textoTiempo = pg.TextItem("test", anchor=(0.5, 0.5), color="k")
textoTiempo.setFont(font2)
GrafTiempo.addItem(textoTiempo)


def update_tiempo(valor):
    textoTiempo.setText('')
    textoTiempo.setText(str(valor[0]))


l2.nextRow()
# Grafico de la batería
GrafBateria = l2.addPlot(title="bateria")
GrafBateria.hideAxis('bottom')
GrafBateria.hideAxis('left')
textoBateria = pg.TextItem("test", anchor=(0.5, 0.5), color="k")
textoBateria.setFont(font2)
GrafBateria.addItem(textoBateria)


def update_bateria(valor):
    pass


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

DatosAcelX = np.linspace(0, 0)
DatosAcelY = np.linspace(0, 0)
DatosAcelZ = np.linspace(0, 0)
ptr2 = 0


def update_acc(valor):
    global curvaAcelX, curvaAcelY, curvaAcelZ, DatosAcelX, DatosAcelY, DatosAcelZ, ptr2
    DatosAcelX[:-1] = DatosAcelX[1:]
    DatosAcelY[:-1] = DatosAcelY[1:]
    DatosAcelZ[:-1] = DatosAcelZ[1:]

    DatosAcelX[-1] = float(valor[8])
    DatosAcelY[-1] = float(valor[9])
    DatosAcelZ[-1] = float(valor[10])
    ptr2 += 1

    curvaAcelX.setData(DatosAcelX)
    curvaAcelY.setData(DatosAcelY)
    curvaAcelZ.setData(DatosAcelZ)

    curvaAcelX.setPos(ptr2, 0)
    curvaAcelY.setPos(ptr2, 0)
    curvaAcelZ.setPos(ptr2, 0)


GrafEuler = l3.addPlot(title="Angulos Euler")
GrafEuler.hideAxis('bottom')
# añadiendo leyenda
GrafEuler.addLegend()
curvaPitch = GrafEuler.plot(pen="r", name="Pitch")
curvaRoll = GrafEuler.plot(pen="g", name="Roll")
curvaYaw = GrafEuler.plot(pen="b", name="Yaw")

DatosPitch = np.linspace(0, 0)
DatosRoll = np.linspace(0, 0)
DatosYaw = np.linspace(0, 0)
ptr3 = 0


def update_gyro(valor):
    global curvaPitch, curvaRoll, curvaYaw, DatosPitch, DatosRoll, DatosYaw, ptr3
    DatosPitch[:-1] = DatosPitch[1:]
    DatosRoll[:-1] = DatosRoll[1:]
    DatosYaw[:-1] = DatosYaw[1:]

    DatosPitch[-1] = float(valor[5])
    DatosRoll[-1] = float(valor[6])
    DatosYaw[-1] = float(valor[7])

    ptr3 += 1

    curvaPitch.setData(DatosPitch)
    curvaRoll.setData(DatosRoll)
    curvaYaw.setData(DatosYaw)

    curvaPitch.setPos(ptr3, 0)
    curvaRoll.setPos(ptr3, 0)
    curvaYaw.setPos(ptr3, 0)


# Graficos de valocidad, temperatura y presion
l4 = Grafico.addLayout(colspan=1, border=(50, 0, 0))
l4.setContentsMargins(10, 10, 10, 10)

GrafVel = l4.addPlot(title="Velocidad", rowspan=2)
GrafVel.hideAxis('bottom')
GrafVel.hideAxis('left')
textoVel = pg.TextItem("test", anchor=(0.5, 0.5), color="k")
textoVel.setFont(font)
GrafVel.addItem(textoVel)

GrafTemp = l4.addPlot(title="Temperatura")
GrafTemp.hideAxis('bottom')
GrafTemp.hideAxis('left')
textoTemp = pg.TextItem("test", anchor=(0.5, 0.5), color="k")
textoTemp.setFont(font2)
GrafTemp.addItem(textoTemp)

l4.nextRow()
GrafPress = l4.addPlot(title="Presion")
GrafPress.hideAxis('bottom')
GrafPress.hideAxis('left')
textoPress = pg.TextItem("test", anchor=(0.5, 0.5), color="k")
textoPress.setFont(font2)
GrafPress.addItem(textoPress)


def update():
    valor = []
    valor = ser.getData()
    update_altura(valor)
    # update_texto_altura()
    update_tiempo(valor)
    update_acc(valor)
    update_gyro(valor)
    # desconozco si es necesario esto
    # QtGui.QApplication.processEvents()


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(500)

# Start Qt event loop unless running in interactive mode.

if __name__ == '__main__':

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
