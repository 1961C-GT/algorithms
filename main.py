import sys
import importlib

import csv
import tkinter as tk
from tkinter import *

from node import Node
from measurement import Measurement

width = 650
height = 650

print("Node Defs: " + sys.argv[1])
print("Data File: " + sys.argv[2])
print("Algorithm: " + sys.argv[3])

#
# Import algorithm
#

alg_name = sys.argv[3]
alg_module = importlib.import_module('Algorithms.' + alg_name + '.' + alg_name)
algorithm = getattr(alg_module, alg_name)

#
# Set up graphics
#

root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, borderwidth=0,
                   highlightthickness=0, bg="black")
canvas.grid()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
# filemenu.add_command(label="Save", command=screenshot, accelerator="Cmd+s")
# filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit, accelerator="Cmd+q")
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


tk.Canvas.create_circle = _create_circle

#
# Import node definitions
#

nodes = {}

with open(sys.argv[1], 'r') as defs_file:
    defs_file.readline()
    node_defs = csv.reader(defs_file)
    for node in node_defs:
        if node[2] == '1':  # node.isBase
            nodes[node[0]] = Node(node[0], node[1], True,
                                  float(node[3]), float(node[4]))
        else:
            nodes[node[0]] = Node(node[0], node[1], False)

#
# Import measurements
#

with open(sys.argv[2], 'r') as data_file:
    data_file.readline()
    measurements = csv.reader(data_file)
    for m in measurements:
        nodes[m[0]].add_measurement(nodes[m[1]], float(m[2]))

#
# Simulate!
#


def render(nodes):
    for key, node in nodes.items():
        node.show(canvas)
    root.wm_title(f"Algorithm Result [{sys.argv[3]}]")
    root.mainloop()

algorithm(nodes)._process(render, canvas)
