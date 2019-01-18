import sys
import importlib

import csv
import tkinter as tk
from tkinter import font
from tkinter import *

from node import Node
from measurement import Measurement

width = 700
height = 700

print("Node Defs: " + sys.argv[1])
print("Algorithm: " + sys.argv[2])

# python3 main.py random example_alg

#
# Import algorithm
#

alg_name = sys.argv[2]
alg_module = importlib.import_module('algorithms.' + alg_name + '.' + alg_name)
algorithm = getattr(alg_module, alg_name)

#
# Set up graphics
#

root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, borderwidth=0,
                   highlightthickness=0, bg="#22252b")
canvas.grid(column=0,row=0, columnspan=30)
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="Save", command=screenshot, accelerator="Cmd+s")
# filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit, accelerator="Cmd+q")
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

T = Text(root, height=2, font = font.Font(family='Courier New', size=14))
T.grid(column=0,row=1)


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


tk.Canvas.create_circle = _create_circle

#
# Import node definitions
#

nodes = {}

with open('./datasets/' + sys.argv[1]+'.def', 'r') as defs_file:
    defs_file.readline()
    node_defs = csv.reader(defs_file)
    for node in node_defs:
        if node[2] == '1':  # node.isBase
            nodes[node[0]] = Node(node[0], node[1], True,
                                  float(node[3]), float(node[4]))
        else:
            nodes[node[0]] = Node(node[0], node[1], False, float(node[3]), float(node[4]))

#
# Import measurements
#

with open('./datasets/' + sys.argv[1]+'.dat', 'r') as data_file:
    data_file.readline()
    measurements = csv.reader(data_file)
    for m in measurements:
        nodes[m[0]].add_measurement(nodes[m[1]], float(m[2]))

with open('./datasets/landscape.csv', 'r') as data_file:
    data_file.readline()
    line = csv.reader(data_file)
    vals = []
    for l in line:
        vals = vals + l
    canvas.create_polygon(vals, fill='#292c34', width=2)

#
# Simulate!
#


def render(nodes, time_taken, note):
    for key, node in nodes.items():
        node.show_real(canvas)
        node.show(canvas)
    root.wm_title(f"Algorithm Result [{sys.argv[2]}]")
    t = "%.2fms" % (time_taken*1000)
    l1 = "Algorithm      : {:17s} || # Elements : {:20s}".format(sys.argv[2], str(len(nodes)))
    l2 = "Execution Time : {:17s} || # Note     : {:20s}".format(t, note)
    T.insert(END, f"{l1}\n{l2}\n")
    root.mainloop()

algorithm(nodes)._process(render, canvas)
