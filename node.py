import uuid
import random
from measurement import Measurement
from tkinter import font
import tkinter as tk


class Node:

    node_objs = {}

    def __init__(self, id=None, name=None, isBase=False, x=None, y=None):
        if id is None:
            id = uuid.uuid4()
        if name is None:
            name = ""
        self.id = id
        self.name = name
        self.isBase = isBase
        self.real_x = x  # random.randint(25, 600)
        self.real_y = y  # random.randint(25, 600)
        if isBase:
            self.x = x
            self.y = y
        else:
            self.x = None
            self.y = None
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

    @staticmethod
    def nodeEnter(event):
        txt = ""
        try:
            txt = __class__.node_objs[event.widget.find_closest(event.x, event.y)[0]]
            __class__.obj = event.widget.create_text(event.x, event.y-20, text=txt,
                fill="white", font=font.Font(family='Courier New', size=14),
                justify=tk.LEFT)
        except:
            pass

    @staticmethod
    def nodeLeave(event):
        try:
            event.widget.delete(__class__.obj)
        except:
            pass

    def show(self, canvas):
        if(self.x is None or self.y is None):
            return
        fill = "white"
        size = 5
        if self.isBase:
            fill = "orange"
            size = 7
        obj = canvas.create_circle(self.x, self.y, size, fill=fill, outline="")
        self.__class__.node_objs[obj] = 'Guess: ' + str(self)
        canvas.tag_bind(obj, '<Enter>', self.__class__.nodeEnter)
        canvas.tag_bind(obj, '<Leave>', self.__class__.nodeLeave)

    def show_real(self, canvas):
        if(self.real_x is None or self.real_y is None):
            return
        fill = "#373B41"
        size = 5
        if self.isBase:
            fill = "#5f2f00"
            size = 7
        obj = canvas.create_circle(self.real_x, self.real_y, size, fill=fill, outline="")
        self.__class__.node_objs[obj] = 'Real: ' + str(self)
        canvas.tag_bind(obj, '<Enter>', self.__class__.nodeEnter)
        canvas.tag_bind(obj, '<Leave>', self.__class__.nodeLeave)

    def get_measurements(self):
        return self.measurements

    def clear_measurements(self):
        self.measurements = []

    def __str__(self):
        if self.name != "":
            return "{name} ({id})".format(name=self.name, id=self.id)
        else:
            return str(self.id)
