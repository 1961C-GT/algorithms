import uuid
import random
from measurement import Measurement
from algorithms.algorithm import Vector2, Distance
from tkinter import font, Canvas
import tkinter as tk


class Node:

    node_arr = {}

    def __init__(self, id=None, name=None, is_base=False, x=None, y=None):
        if id is None:
            id = uuid.uuid4()
        if name is None:
            name = ""
        self.id = id
        self.name = name
        self.is_base = is_base
        self.real_x = x  # random.randint(25, 600)
        self.real_y = y  # random.randint(25, 600)
        self.real_obj = None
        self.guess_obj = None
        self.resolved = False
        self.triangulate_list = []
        if is_base:
            self.x = x
            self.y = y
            self.resolved = True
        else:
            self.x = None
            self.y = None
        self.measurements = []

    def add_measurement(self, node_b, dist):
        self.measurements.append(Measurement(self, node_b, dist))
    
    def isResolved(self):
        return self.resolved

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.resolved = True

    def addTriangulation(self, tri):
        self.triangulate_list.append(tri)

    def getTriangulations(self):
        return self.triangulate_list

    def displayTriangulations(self, canvas):
        for dt in self.triangulate_list:
            dt.displayTriangulation(canvas, (self.x, self.y))

    def set_position_vec(self, pos):
        self.x = pos.x
        self.y = pos.y
        self.resolved = True

    def get_position(self):
        return (self.x, self.y)

    def get_position_vec(self):
        return Vector2(self.x, self.y)

    def get_real_position(self):
        return (self.real_x, self.real_y)

    def get_real_position_vec(self):
        return Vector2(self.real_x, self.real_y)

    @staticmethod
    def nodeEnter(event):

        draft = Canvas(event.widget)  # if w is deleted, the draft is deleted
        draft.delete("all")  # if you use the fake canvas for other uses

        concerned = event.widget.find_withtag("node")  # what you want
        for obj in concerned:  # copy on draft
            # first, get the method to use
            if event.widget.type(obj) == "oval":
                create = draft.create_oval
            # use "elif ..." to copy more types of objects
            else:
                continue
            # copy the element with its attributes
            config = {opt: event.widget.itemcget(
                obj, opt) for opt in event.widget.itemconfig(obj)}
            # I can retrieve the ID in "w" later with this trick
            config["tags"] = str(obj)
            create(*event.widget.coords(obj), **config)
        # use coordinates relative to the canvas
        x = event.widget.canvasx(event.x)
        y = event.widget.canvasy(event.y)
        item = draft.find_closest(x, y)  # ID in draft (as a tuple of len 1)
        if item:
            item = int(draft.gettags(*item)[0])  # ID in w
        else:
            item = None  # closest not found
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
        if(self.x is None or self.y is None or self.is_base is True):
            return
        fill = "white"
        if Distance(self.get_real_position_vec(), self.get_position_vec()) < 20:
            fill = "green"
        size = 10
        obj = canvas.create_circle(
            self.x, self.y, size, fill=fill, outline="", tags=['node'])
        if self.real_obj is not None:
            coords = canvas.coords(self.real_obj)
            x = (coords[0] + coords[2])/2
            y = (coords[1] + coords[3])/2
            canvas.create_line(self.x, self.y, x, y,
                               fill="#3c4048", dash=(3, 5))
            canvas.tag_raise(obj)
            canvas.tag_raise(self.real_obj)
        self.guess_obj = obj
        self.__class__.node_arr[obj] = str(self) + ' : ' + self.errorToStr()
        canvas.tag_bind(obj, '<Enter>', self.__class__.nodeEnter)
        canvas.tag_bind(obj, '<Leave>', self.__class__.nodeLeave)

    def show_real(self, canvas):
        if(self.real_x is None or self.real_y is None):
            return
        fill = "#373B41"
        if not self.is_base and Distance(self.get_real_position_vec(), self.get_position_vec()) < 20:
            return
        size = 10
        if self.is_base:
            fill = "orange"
            size = 20
        obj = canvas.create_circle(
            self.real_x, self.real_y, size, fill=fill, outline="", tags=['node'])
        if self.guess_obj is not None:
            coords = canvas.coords(self.guess_obj)
            x = (coords[0] + coords[2])/2
            y = (coords[1] + coords[3])/2
            canvas.create_line(self.real_x, self.real_y, x,
                               y, fill="#3c4048", dash=(3, 5))
            canvas.tag_raise(obj)
            canvas.tag_raise(self.guess_obj)
        self.real_obj = obj
        self.__class__.node_arr[obj] = 'Real: ' + str(self)
        canvas.tag_bind(obj, '<Enter>', self.__class__.nodeEnter)
        canvas.tag_bind(obj, '<Leave>', self.__class__.nodeLeave)

    def errorToStr(self):
        if self.x is not None and self.y is not None:
            offset = self.get_position_vec() - self.get_real_position_vec()
            d = offset.magnitude()
            return "{:.3f}ft".format(d)
        else:
            return "Unresolved"

    def printReport(self):
        if self.x is not None and self.y is not None:
            print(str(self), " : ", self.errorToStr() + ' error')

    def get_measurement(self, node_id):
        return next(filter(lambda m: m.node2.id == node_id, self.measurements))

    def get_measurements(self):
        return self.measurements

    def clear_measurements(self):
        self.measurements = []

    def getAsString(self):
        if self.x is not None and self.y is not None:
            str1 = "{name} ({id}) -> x: ".format(name=self.name, id=self.id)
            return str1 + "{:.3f}, y: {:.3f}".format(self.x, self.y)
        else:
            return str(self)

    def __str__(self):
        if self.name != "":
            return "{name} ({id})".format(name=self.name, id=self.id)
        else:
            return str(self.id)
