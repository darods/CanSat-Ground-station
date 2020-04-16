import time
import csv


class db():
    def __init__(self):
        pass

    def guardar(self, dato):
        dato.append(time.asctime())
        with open("flight_data.csv", "a") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(dato)
