# GUI Estación terrestre para CanSat u OBC's
Código de una GUI para una estación terrestre para CanSats y/o OBCs donde se muestran los datos de diferentes sensores en tiempo real. **No se necesitan sensores para probarlo**.

![imagen](https://i.imgur.com/zDY3DnY.gif)

## Tabla de contenidos
* [Apoyo](#apoyo)
* [Información general](#informacion-general)
* [Liberias](#librerias)
* [Configuración Linux](#configuracion-linux)
* [Configuración Windows](#configuracion-windows)
* [¿Cómo funciona?](#como-funciona)
* [Fuentes](#fuentes)
* [Licencia](#licencia)

___
## Apoyo
Si usaste este proyecto o aprendiste algo, por favor dale una estrella a este proyecto para seguir haciendo proyectos de código abierto.
___

## Informacion general
El propósito de este proyecto es hacer una GUI en la que los datos transmitidos por un OBC (ordenador de a bordo) o un CanSat sean comprensibles a primera vista a través de una cadena de texto en un puerto serie.

Este proyecto está fuertemente relacionado con
otro proyecto de [ciencia de cohetes y CanSat](https://github.com/el-NASA/POA). **Está todavía en desarrollo.**

### Bugs
* La mayoría de las veces los elementos de texto desaparecen, los invito a resolver esto.

* A veces no puede convertir el primer valor de la lista a int, pero se resuelve solo al volver a ejecutarlo.

* el gráfico de velocidad está en desarrollo, crece hasta el infinito.
___
## Librerias
El proyecto se crea con:
* numpy==1.22.4
* PyQt5==5.15.6
* PyQt5-Qt5==5.15.2
* PyQt5-sip==12.10.1
* pyqtgraph==0.12.4
* pyserial==3.5


___
## Configuracion Linux
Para poder ejecutarlo tienes que abrir la terminal en la carpeta y escribir:
```
$ virtualenv env
$ fuente env/bin/activate
$ pip3 install -r requiments.txt
$ python3 main.py
```
Si no tienes la electrónica aun puedes probarla! Cuando la terminal te pide que escribas un puerto serie, escribe cualquier cosa y funcionará, graficará datos aleatorios. (pero el error de texto permanece ;v).
___

## Configuracion Windows
Abre CMD o PowerShell en la dirección de la carpeta y escribe los siguientes comandos:
```
> virutalenv env
> \env\Scripts\activate.bat
> pip install -r requeriments.txt
> python main.py

```
## ¿Como funciona?
### ¿Cómo toma las muestras?
Cada 500 ms toma una muestra, este número proviene de la tasa de datos que tiene el Arduino, **si no tiene el Arduino y los sensores, la GUI aún funciona, grafica datos aleatorios**. El bucle es:
```
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(500)
```

### Que valores usa?
La función `update()` actualiza los gráficos y el texto de la interfaz. Lo primero que hace es obtener una lista de la información a ser actualizada, esta lista es anotada como un `value_chain`.

Luego, dentro de `update` se ejecutan los métodos *update* específicos para cada elemento que depende de esta lista.

Los valores que recibe son:
0. Tiempo de registro
1. Altura relativa
2. Está en caída libre (0 o 1)
3. Temperatura
4. Presión atmosférica
5. Pitch
6. Rueda
7. Yaw
8. Aceleración en X
9. Aceleración del eje Y
10. Aceleración Z



### ¿Cómo almacena la información?
Pulsando el botón **Start storage** llama a una función de la clase **data_base** que cambia un estado que determina si el método `guardar` escribe la información en la lista. Lo mismo ocurre con el botón **Stop storage**.

En este archivo la lista llamada `value_chain` se almacena en el mismo orden añadiendo al final la fecha que se registra en el ordenador.

___
## Fuentes
"Si he visto más lejos que otros, es por estar parado sobre los hombros de gigantes." - Newton burlándose de la espalda de Hooke.
* Hrisko, J. (2018). [Python Datalogger - Usando pySerial para leer la salida de datos en serie de Arduino.](https://bit.ly/2wQvByM)
* Sepúlveda, S. Reyes, P. Weinstein, A. (2015). [Visualización de señales fisiológicas en tiempo real](https://bit.ly/2XIRzyw). doi: 10.25080/Majora-7b98e3ed-01c
* Golubev, P. (2018). [Ejecutar pyqtgraph en tiempo real en PlotWidget GUI.](https://bit.ly/2VeXSIv)
* Pythonspot.(n.d.). [PyQt5.](https://pythonspot.com/pyqt5/)
* [Sr. Tom](https://bit.ly/3amndEZ). (2016). [Calcular la velocidad en el acelerómetro](https://bit.ly/3acX3nP).
* Selfert, K. Camacho, O. (2007). [Implementar algoritmos de posicionamiento usando acelerómetros](https://bit.ly/2REEH8X). Freescale Semiconductor.
* Muchas otras personas frías en el desbordamiento de la pila.
___
# Licencia
Es [MIT](https://github.com/el-NASA/Estacion-Terrena/blob/master/LICENSE) <3. (por ahora)

Desarrollado por Daniel Alejandro Rodríguez Suárez, líder del semillero de investigación ATL, vinculado al grupo de investigación LIDER de la Universidad Distrital.
