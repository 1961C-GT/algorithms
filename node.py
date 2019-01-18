import uuid
import random
from measurement import Measurement


class Node:
    def __init__(self, id=None, name=None, isBase=False, x=-1, y=-1):
        if id is None:
            id = uuid.uuid4()
        if name is None:
            name = ""
        self.id = id
        self.name = name
        self.isBase = isBase
        self.real_x = x  # random.randint(25, 600)
        self.real_y = y  # random.randint(25, 600)
        self.x = -1
        self.y = -1
        self.measurements = []

    def add_measurement(self, nodeB, dist):
        self.measurements.append(Measurement(self, nodeB, dist))

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def get_real_position(self):
        return (self.real_x, self.real_y)

    def show(self, canvas):
        fill = "white"
        size = 5
        if self.isBase:
            fill = "orange"
            size = 10
        canvas.create_circle(self.x, self.y, size, fill=fill)

    def show_real(self, canvas):
        fill = "#444444"
        size = 5
        if self.isBase:
            fill = "#5f2f00"
            size = 10
        canvas.create_circle(self.real_x, self.real_y, size, fill=fill)

    def get_measurements(self):
        return self.measurements

    def clear_measurements(self):
        self.measurements = []

    def __str__(self):
        if self.name != "":
            return "{name} ({id})".format(name=self.name, id=self.id)
        else:
            return str(self.id)
