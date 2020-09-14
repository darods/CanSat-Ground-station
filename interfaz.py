from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from comunicacion import Comunicacion
import math
from dataBase import db
from PyQt5.QtWidgets import QPushButton

pg.setConfigOption('background', (33, 33, 33))
pg.setConfigOption('foreground', (197, 198, 199))
# Variables de la interfaz
app = QtGui.QApplication([])
view = pg.GraphicsView()
Grafico = pg.GraphicsLayout()
view.setCentralItem(Grafico)
view.show()
view.setWindowTitle('Monitoreo de vuelo')
view.resize(1200, 700)

# se declara la clase que se comunica con el puerto serial
ser = Comunicacion()
# clase que guarda en un archivo csv
db = db()
# Fuentes para mostrar solo un numero
font = QtGui.QFont()
font.setPixelSize(90)


# Title at top
text = """
Interfaz de monitoreo de vuelo para cansats y OBC's <br>
desarrollados en la Universidad Distrital FJC.
"""
Grafico.addLabel(text, col=1, colspan=21)
Grafico.nextRow()

# Put vertical label on left side
Grafico.addLabel('LIDER - Semillero de investigación ATL',
                 angle=-90, rowspan=3)

Grafico.nextRow()
# botones de guardar datos

# estilo de los botones
estilo = "background-color:rgb(29, 185, 84);color:rgb(0,0,0);font-size:14px;"

lb = Grafico.addLayout(colspan=21)
proxy = QtGui.QGraphicsProxyWidget()
b_ini_guardar = QtGui.QPushButton('iniciar almacenamiento')
b_ini_guardar.setStyleSheet(estilo)
b_ini_guardar.clicked.connect(db.iniciar)
proxy.setWidget(b_ini_guardar)
lb.addItem(proxy)
lb.nextCol()


proxy2 = QtGui.QGraphicsProxyWidget()
b_fin_guardar = QtGui.QPushButton('detener almacenamiento')
b_fin_guardar.setStyleSheet(estilo)
b_fin_guardar.clicked.connect(db.detener)
proxy2.setWidget(b_fin_guardar)
lb.addItem(proxy2)


Grafico.nextRow()

# Grafico de altitud
l1 = Grafico.addLayout(colspan=20, rowspan=2)
l11 = l1.addLayout(rowspan=1, border=(83, 83, 83))
# l1.setContentsMargins(10, 10, 10, 10)
p1 = l11.addPlot(title="Altura (m)")
# p1.hideAxis('bottom')
curva_altura = p1.plot(pen=(29, 185, 84))
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
p2 = l11.addPlot(title="Velocidad (m/s)")
curva_vel = p2.plot(pen=(29, 185, 84))
datos_vel = np.linspace(0, 0, 30)
ptr6 = 0
vx = 0
vy = 0
vz = 0
vel = 0


def update_vel(valor):
    global curva_vel, datos_vel, ptr6, vx, vy, vz, vel
    # 500 es dt
    i = 0
    if(i == 0):
        vzo = float(valor[10])
        i += 1

    vx += (float(valor[8])) * 500
    vy += (float(valor[9])) * 500
    vz += (float(valor[10]) - vzo) * 500
    sum = math.pow(vx, 2) + math.pow(vy, 2) + math.pow(vz, 2)
    vel = math.sqrt(sum)
    datos_vel[:-1] = datos_vel[1:]
    datos_vel[-1] = vel
    ptr6 += 1
    curva_vel.setData(datos_vel)
    curva_vel.setPos(ptr6, 0)


l1.nextRow()
l12 = l1.addLayout(rowspan=1, border=(83, 83, 83))

# Grafico de aceleraciones
GrafAcel = l12.addPlot(title="Aceleraciones (m/s²)")
# añadiendo leyenda
GrafAcel.addLegend()
GrafAcel.hideAxis('bottom')
curvaAcelX = GrafAcel.plot(pen=(102, 252, 241), name="X")
curvaAcelY = GrafAcel.plot(pen=(29, 185, 84), name="Y")
curvaAcelZ = GrafAcel.plot(pen=(203, 45, 111), name="Z")

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
GrafEuler = l12.addPlot(title="Gyro")
GrafEuler.hideAxis('bottom')
# añadiendo leyenda
GrafEuler.addLegend()
curvaPitch = GrafEuler.plot(pen=(102, 252, 241), name="Pitch")
curvaRoll = GrafEuler.plot(pen=(29, 185, 84), name="Roll")
curvaYaw = GrafEuler.plot(pen=(203, 45, 111), name="Yaw")

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
curva_presion = graf_presion.plot(pen=(102, 252, 241))
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
graf_temp = l12.addPlot(title="Temperatura (ºc)")
curva_temp = graf_temp.plot(pen=(29, 185, 84))
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
l2 = Grafico.addLayout(border=(83, 83, 83))


# Grafico del tiempo
GrafTiempo = l2.addPlot(title="Tiempo (min)")
GrafTiempo.hideAxis('bottom')
GrafTiempo.hideAxis('left')
textoTiempo = pg.TextItem("test", anchor=(0.5, 0.5), color="w")
textoTiempo.setFont(font)
GrafTiempo.addItem(textoTiempo)


def update_tiempo(valor):
    global textoTiempo
    textoTiempo.setText('')
    tiempo = round(int(valor[0]) / 60000, 2)
    textoTiempo.setText(str(tiempo))


l2.nextRow()

# Grafico de la batería
GrafBateria = l2.addPlot(title="bateria")
GrafBateria.hideAxis('bottom')
GrafBateria.hideAxis('left')
textoBateria = pg.TextItem("test", anchor=(0.5, 0.5), color="w")
textoBateria.setFont(font)
GrafBateria.addItem(textoBateria)


def update_bateria(valor):
    pass


l2.nextRow()

graf_clibre = l2.addPlot(title="caida libre")
graf_clibre.hideAxis('bottom')
graf_clibre.hideAxis('left')
text_clibre = pg.TextItem("test", anchor=(0.5, 0.5), color="w")
text_clibre.setFont(font)
graf_clibre.addItem(text_clibre)


def update_clibre(valor):
    global text_clibre
    text_clibre.setText('')
    if(valor[2] == '0'):
        text_clibre.setText('No')
    else:
        text_clibre.setText('Si')


def update():
    try:
        valor = []
        valor = ser.getData()
        update_altura(valor)
        update_vel(valor)
        update_tiempo(valor)
        update_acc(valor)
        update_gyro(valor)
        update_presion(valor)
        update_temp(valor)
        update_clibre(valor)
        db.guardar(valor)
    except IndexError:
        print('iniciando')

    # desconozco si es necesario esto
    # QtGui.QApplication.processEvents()


if(ser.isOpen()) or (ser.dummyMode()):
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
