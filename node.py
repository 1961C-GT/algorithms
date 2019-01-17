import uuid
import random
from measure import Measurement

class Node:
    def __init__(self, id=None, name=None, base=False, x=0, y=0):
        if id is None:
            id = uuid.uuid4()
        if name is None:
            name = ""
        self.id = id;
        self.measurements = []
        self.base = base
        self.x = x #random.randint(25, 600)
        self.y = y #random.randint(25, 600)
        self.name = name

    def addMeasurement(self, nodeb, dist):
        self.measurements.append(Measurement(self, nodeb, dist))

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        return (self.x, self.y)

    def show(self, canvas):
        fill = "white"
        size = 5
        if self.base:
            fill="orange"
            size = 10
        canvas.create_circle(self.x, self.y, size, fill=fill)

    def getMeasurements(self):
        return self.measurements

    def clearMeasurement(self):
        self.measurements = []

    def __str__(self):
        if self.name != "":
            return str(self.name) + ":" + str(self.id)
        else:
            return str(self.id)
