import sys
import importlib

import csv
import tkinter as tk

from node import Node
from measurement import Measurement

print("Node Defs: " + sys.argv[1])
print("Data File: " + sys.argv[2])
print("Algorithm: " + sys.argv[3])

#
# Import algorithm
#

alg_name = sys.argv[3]
alg_module = importlib.import_module('algorithms.' + alg_name + '.' + alg_name)
algorithm = getattr(alg_module, alg_name)

#
# Set up graphics
#

root = tk.Tk()
canvas = tk.Canvas(root, width=650, height=650, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()
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
        if node[2] == '1': # node.isBase
            nodes[node[0]] = Node(node[0], node[1], True, float(node[3]), float(node[4]))
        else:
            nodes[node[0]] = Node(node[0], node[1], False)

#
# Import measurements
#

with open(sys.argv[2], 'r') as data_file:
    data_file.readline()
    measurements = csv.reader(data_file)
    for m in measurements:
        nodes[m[0]].addMeasurement(nodes[m[1]], float(m[2]))

#
# Simulate!
#

def render(nodes):
    for key, node in nodes.items():
        node.show(canvas)
    root.wm_title("Circles and Arcs")
    root.mainloop()

algorithm(nodes)._process(render)
