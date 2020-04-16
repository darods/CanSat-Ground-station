import time
import csv


class db():
    def __init__(self):
        self.estado = False

    def guardar(self, dato):
        if self.estado == True:
            dato.append(time.asctime())
            with open("flight_data.csv", "a") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerow(dato)

    def iniciar(self):
        self.estado = True
        print('iniciando almacenamiento en csv')

    def detener(self):
        self.estado = False
        print('deteniendo almacenamiento en csv')
