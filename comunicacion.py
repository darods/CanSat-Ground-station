import serial
import serial.tools.list_ports


class Comunicacion:
    baudrate = ''
    portName = ''
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

    def cerrar(self):
        if(self.ser.isOpen()):
            self.ser.close()
        else:
            print("ya esta cerrado")

    def getData(self):
        value = self.ser.readline()  # read line (single value) from the serial port
        decoded_bytes = str(value[0:len(value) - 2].decode("utf-8"))
        # print(decoded_bytes)
        valor = decoded_bytes.split(",")
        return valor
