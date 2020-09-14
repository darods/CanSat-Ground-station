import random
import serial
import serial.tools.list_ports


class Comunicacion:
    baudrate = ''
    portName = ''
    dummyPlug= False
    ports = serial.tools.list_ports.comports()
    ser = serial.Serial()

    def __init__(self):
        self.baudrate = 9600
        print("los puertos disponibles son: ")
        for port in sorted(self.ports):
            # obtener la lista de puetos: https://stackoverflow.com/a/52809180
            print(("{}".format(port)))
        self.portName = input("escribe el puerto serial (ej: /dev/ttyUSB0): ")
        try:
            self.ser = serial.Serial(self.portName, self.baudrate)
        except serial.serialutil.SerialException:
            print("no se pudo abrir : ", self.portName)
            self.dummyPlug = True
            print("Dummy mode activated")

    def cerrar(self):
        if(self.ser.isOpen()):
            self.ser.close()
        else:
            print("ya esta cerrado")

    def getData(self):
        if(self.dummyMode == False):
            value = self.ser.readline()  # read line (single value) from the serial port
            decoded_bytes = str(value[0:len(value) - 2].decode("utf-8"))
            # print(decoded_bytes)
            valor = decoded_bytes.split(",")
        else:
            valor = [0]+random.sample(range(0,300),1)+[random.getrandbits(1)]+random.sample(range(0,20),8)
        return valor

    def isOpen(self):
        return self.ser.isOpen()

    def dummyMode(self):
        return self.dummyPlug
