import uuid
import random
from measure import Measurement

class Node:
    def __init__(self, id=None, base=False):
        if id is None:
            id = uuid.uuid4()
        self.id = id;
        self.measurements = []
        self.base = base
        self.x = 0 #random.randint(25, 600)
        self.y = 0 #random.randint(25, 600)

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
        if self.base:
            return 'Base: ' + str(self.id)
        else:
            return 'Node: ' + str(self.id)
