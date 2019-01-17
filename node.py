import uuid
import random
from measure import Measurement

class Node:
    def __init__(self, id=None, name=None, isBase=False, x=0, y=0):
        if id is None:
            id = uuid.uuid4()
        if name is None:
            name = ""
        self.id = id;
        self.name = name
        self.isBase = isBase
        self.x = x #random.randint(25, 600)
        self.y = y #random.randint(25, 600)
        self.measurements = []

    def addMeasurement(self, nodeB, dist):
        self.measurements.append(Measurement(self, nodeB, dist))

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def getPosition(self):
        return (self.x, self.y)

    def show(self, canvas):
        fill = "white"
        size = 5
        if self.isBase:
            fill = "orange"
            size = 10
        canvas.create_circle(self.x, self.y, size, fill=fill)

    def getMeasurements(self):
        return self.measurements

    def clearMeasurements(self):
        self.measurements = []

    def __str__(self):
        if self.name != "":
            return "{name} ({id})".format(name=self.name, id=self.id)
        else:
            return str(self.id)
