# Ground station GUI for CanSat or OBC's
Code for a CanSat or OBCs GUI ground station where different sensor data are displayed in real time. **No sensors needed to try it**.
**2022 jun update**.

![imagen](https://i.imgur.com/zDY3DnY.gif)

## Table of contents
* [Support](#support)
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup Linux](#setup-linux)
* [Setup Windows](#setup-windows)
* [How does it work?](#how-does-it-work)
* [Sources](#sources)
* [Licence](#licence)

___
## Support
If you used this project or learned something please give this project a star to keep doing open source projects
___

## General info
The purpose of this project is to make a GUI for the data transmitted by an OBC (on board computer) or a CanSat understandable at first sight through a text string on a serial port.


This project is strongly related to
another [rocket science and CanSat](https://github.com/el-NASA/POA) project. **It's still in development.**

### Bugs
* Most of the times the text items disappear, i invite you to solve this.

* Sometimes it can't convert the first value of the list to int, but it solves it self by re-running it.

* the speed graph is under development, it grows to infinity.
___
## Technologies
Project is created with:
* numpy==1.22.4
* PyQt5==5.15.6
* PyQt5-Qt5==5.15.2
* PyQt5-sip==12.10.1
* pyqtgraph==0.12.4
* pyserial==3.5

___
## Setup Linux
To be able to run it you have to open the terminal in the folder and type:
```
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
$ python3 main.py
```
if you don't have the electronics you can still use it! When the terminal asks you to write a serial port, write anything and it will work, it will display random data. (but the text bug remains ;v).
___

## Setup Windows
Open CMD or PowerShell in the folder and type:
```
> virtualenv env
> \env\Scripts\activate.bat
> pip install -r requirements.txt
> python main.py
```

## How does it work?
### How does it sample?
Every 500 ms takes a sample, this number comes from the data rate that the Arduino has **if you don't have the Arduino and Sensors, the GUI still works, it graphs random data**. The loop is:
```
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(500)
```

### What values uses?
The `update()` function updates the graphics and text of the interface. The first thing it does is get a list of the information to be updated, this list is noted as a `value_chainr`.

Then within `update` you execute the *update* methods specific to each element that depends on this list.

The values it receives are:
0. Logging time
1. Relative height
2. Is in free fall (0 or 1)
3. Temperature
4. Atmospheric pressure
5. Pitch
6. Roll
7. Yaw
8. Acceleration in X
9. Y-axis acceleration
10. Z-acceleration


### How does it store the information?
Clicking on the **Start storage** button calls a function of the **data_base** class that changes a state that determines whether the `guardar` method writes the information in the list. The same happens with the **Stop storage** button.

In this file the list called `value_chain` is stored in the same order adding at the end the date that is registered in the computer.

___
## Sources
"If I have seen further than others, it is by standing upon the shoulders of giants." - newton making fun of hooke's back.
* Hrisko, J. (2018). [Python Datalogger - Using pySerial to Read Serial Data Output from Arduino.](https://bit.ly/2wQvByM)
* Sepúlveda, S. Reyes, P. Weinstein, A. (2015). [Visualizing physiological signals in real-time](https://bit.ly/2XIRzyw). doi: 10.25080/Majora-7b98e3ed-01c
* Golubev, P. (2018). [Run Real-time pyqtgraph in PlotWidget GUI.](https://bit.ly/2VeXSIv)
* Pythonspot.(n.d). [PyQt5.](https://pythonspot.com/pyqt5/)
* [Mr. Tom](https://bit.ly/3amndEZ). (2016). [Calculate speed from accelerometer](https://bit.ly/3acX3nP).
* Selfert, K. Camacho, O. (2007). [Implementing Positioning Algorithms Using Accelerometers](https://bit.ly/2REEH8X). Freescale Semiconductor.
* Many other cool people on stack overflow.
___
# Licence
It's [MIT](https://github.com/el-NASA/Estacion-Terrena/blob/master/LICENSE) <3. (for now)

Developed by Daniel Alejandro Rodriguez Suarez, leader of the ATL research seedbed, linked to the Universidad Distrital's LIDER research group.
