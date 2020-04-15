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
view.resize(1200, 700)

ser = Comunicacion()

# Fuentes para mostrar solo un numero
font = QtGui.QFont()
font.setPixelSize(120)

font2 = QtGui.QFont()
font2.setPixelSize(90)


# Title at top
text = """
Interfaz de monitroreo de vuelo para cansats y OBC's <br>
desarrollados en la Universidad Distrital FJC.
"""
Grafico.addLabel(text, col=1, colspan=21)
Grafico.nextRow()

# Put vertical label on left side
Grafico.addLabel('LIDER - Semillero de investigación ATL',
                 angle=-90, rowspan=2)


# Grafico de altitud
l1 = Grafico.addLayout(colspan=20, rowspan=2)
l11 = l1.addLayout(rowspan=1, border=(0, 0, 0))
# l1.setContentsMargins(10, 10, 10, 10)
p1 = l11.addPlot(title="Altura")
# p1.hideAxis('bottom')
curva_altura = p1.plot(pen="r")
datos_altura = np.linspace(0, 0, 30)
ptr1 = 0


def update_altura(valor):
    global curva_altura, datos_altura,  ptr1
    datos_altura[:-1] = datos_altura[1:]
    # valor = ser.getData()
    datos_altura[-1] = float(valor[1])
    ptr1 += 1
    curva_altura.setData(datos_altura)
    curva_altura.setPos(ptr1, 0)


# grafico de la Velocidad
p2 = l11.addPlot(title="Velocidad")
curva_vel = p2.plot(pen="b")

l1.nextRow()
l12 = l1.addLayout(rowspan=1, border=(0, 0, 0))


# Grafico de aceleraciones
GrafAcel = l12.addPlot(title="Aceleraciones")
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


# Grafico del gyro
GrafEuler = l12.addPlot(title="Angulos Euler")
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


# Grafico Presion
graf_presion = l12.addPlot(title="Presion barometrica")
curva_presion = graf_presion.plot(pen="r")
datos_presion = np.linspace(0, 0, 30)
ptr4 = 0


def update_presion(valor):
    global curva_presion, datos_presion,  ptr4
    datos_presion[:-1] = datos_presion[1:]
    datos_presion[-1] = float(valor[4])
    ptr4 += 1
    curva_presion.setData(datos_presion)
    curva_presion.setPos(ptr4, 0)


# Grafico temperatura
graf_temp = l12.addPlot(title="Temperatura")
curva_temp = graf_temp.plot(pen="r")
datos_temp = np.linspace(0, 0, 30)
ptr5 = 0


def update_temp(valor):
    global curva_temp, datos_temp,  ptr5
    datos_temp[:-1] = datos_temp[1:]
    datos_temp[-1] = float(valor[3])
    ptr5 += 1
    curva_temp.setData(datos_temp)
    curva_temp.setPos(ptr5, 0)


# Graficos de tiempo, bateria y caida
l2 = Grafico.addLayout(border=(0, 0, 0))


# Grafico del tiempo
GrafTiempo = l2.addPlot(title="Tiempo (min)")
GrafTiempo.hideAxis('bottom')
GrafTiempo.hideAxis('left')
textoTiempo = pg.TextItem("test", anchor=(0.5, 0.5), color="k")
textoTiempo.setFont(font2)
GrafTiempo.addItem(textoTiempo)


def update_tiempo(valor):
    textoTiempo.setText('')
    # print(round(int(valor[0]) / 60000, 2), int(valor[0]))
    tiempo = round(int(valor[0]) / 60000, 2)
    textoTiempo.setText(str(tiempo))


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


l2.nextRow()

graf_clibre = l2.addPlot(title="caida libre")
graf_clibre.hideAxis('bottom')
graf_clibre.hideAxis('left')
text_clibre = pg.TextItem("test", anchor=(0.5, 0.5), color="k")
text_clibre.setFont(font2)
graf_clibre.addItem(text_clibre)


def update_clibre(valor):
    pass


def update():
    valor = []
    valor = ser.getData()
    update_altura(valor)
    update_tiempo(valor)
    update_acc(valor)
    update_gyro(valor)
    update_presion(valor)
    update_temp(valor)
    # desconozco si es necesario esto
    # QtGui.QApplication.processEvents()


if(ser.isOpen()):
    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(500)
else:
    print("el puerto no se encuentra abierto")
# Start Qt event loop unless running in interactive mode.

if __name__ == '__main__':

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
