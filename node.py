import uuid
import random
from measurement import Measurement
from tkinter import font, Canvas
import tkinter as tk


class Node:

    node_arr = {}

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
        self.real_obj = None
        self.guess_obj = None
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

        draft = Canvas(event.widget) # if w is deleted, the draft is deleted
        draft.delete("all") # if you use the fake canvas for other uses

        concerned = event.widget.find_withtag("node") # what you want
        for obj in concerned: # copy on draft
            # first, get the method to use
            if event.widget.type(obj) == "oval": create = draft.create_oval
            # use "elif ..." to copy more types of objects
            else: continue
            # copy the element with its attributes
            config = {opt:event.widget.itemcget(obj, opt) for opt in event.widget.itemconfig(obj)}
            config["tags"] = str(obj) # I can retrieve the ID in "w" later with this trick
            create(*event.widget.coords(obj), **config)
        # use coordinates relative to the canvas
        x = event.widget.canvasx(event.x)
        y = event.widget.canvasy(event.y)
        item = draft.find_closest(x,y) # ID in draft (as a tuple of len 1)
        if item: item = int( draft.gettags(*item)[0] ) # ID in w
        else: item = None # closest not found
        if item is None or not item in __class__.node_arr:
            return
        coords = event.widget.coords(item)
        x = (coords[0] + coords[2])/2
        y = (coords[1] + coords[3])/2

        txt = __class__.node_arr[item]
        __class__.obj = event.widget.create_text(x, y-20, text=txt,
            fill="white", font=font.Font(family='Courier New', size=14),
            justify=tk.LEFT)

    @staticmethod
    def nodeLeave(event):
        try:
            event.widget.delete(__class__.obj)
        except:
            pass

    def show(self, canvas):
        if(self.x is None or self.y is None or self.isBase is True):
            return
        fill = "white"
        size = 5
        obj = canvas.create_circle(self.x, self.y, size, fill=fill, outline="", tags=['node'])
        if self.real_obj is not None:
            coords = canvas.coords(self.real_obj)
            x = (coords[0] + coords[2])/2
            y = (coords[1] + coords[3])/2
            canvas.create_line(self.x, self.y, x, y, fill="#3c4048", dash=(3,5))
            canvas.tag_raise(obj)
            canvas.tag_raise(self.real_obj)
        self.guess_obj = obj
        self.__class__.node_arr[obj] = 'Guess: ' + str(self)
        canvas.tag_bind(obj, '<Enter>', self.__class__.nodeEnter)
        canvas.tag_bind(obj, '<Leave>', self.__class__.nodeLeave)

    def show_real(self, canvas):
        if(self.real_x is None or self.real_y is None):
            return
        fill = "#373B41"
        size = 5
        if self.isBase:
            fill = "orange"
            size = 7
        obj = canvas.create_circle(self.real_x, self.real_y, size, fill=fill, outline="",tags=['node'])
        if self.guess_obj is not None:
            coords = canvas.coords(self.guess_obj)
            x = (coords[0] + coords[2])/2
            y = (coords[1] + coords[3])/2
            canvas.create_line(self.real_x, self.real_y, x, y, fill="#3c4048", dash=(3,5))
            canvas.tag_raise(obj)
            canvas.tag_raise(self.guess_obj)
        self.real_obj = obj
        self.__class__.node_arr[obj] = 'Real: ' + str(self)
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
