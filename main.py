#!/usr/bin/env python3

import sys
import importlib
import math

import csv
import tkinter as tk
from tkinter import font
from tkinter import *

from node import Node
from measurement import Measurement

width = 700
height = 700
area_width = 2000
area_height = 2000
move_amt = 20

if len(sys.argv) < 3:
    print("Using default data files...")
    dat_file = "random"
    alg_name = "drct_trng"
else:
    dat_file = sys.argv[1]
    alg_name = sys.argv[2]

print("Data File: " + dat_file)
print("Algorithm: " + alg_name)

# python3 main.py random example_alg

#
# Import algorithm
#

alg_module = importlib.import_module('algorithms.' + alg_name + '.' + alg_name)
algorithm = getattr(alg_module, alg_name)

#
# Set up graphics
#

root = tk.Tk()
# root.resizable(width=False, height=False)
canvas = tk.Canvas(root, width=width, height=height, borderwidth=0,
                   highlightthickness=0, bg="#22252b")
canvas.grid(column=0, row=0, columnspan=30)
# Add menu
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.quit, accelerator="Cmd+q")
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)
# root.attributes('-alpha', 0.8)

# Configure measure utilitity
# Include globals (for event data transfer)
global measuring, start_pos, universal_scale
# Init globals
start_pos = []
measuring = False
universal_scale = 1
# Measure function


def measure(event):
    # Include globals
    global measuring, start_pos, cur_line, cur_line_txt, universal_scale
    # Check to see if we are measuring
    if measuring == True:
        # Try to remove the old elements
        try:
            event.widget.delete(cur_line)
            event.widget.delete(cur_line_txt)
        except:
            pass
        # Calculate the rotation between the two points
        rotation = 180 - math.degrees(math.atan2(start_pos[1] - event.y,
                                                 start_pos[0] - event.x))
        # Normalize the rotation
        if rotation > 90 and rotation < 270:
            rotation -= 180
        # Convert to radians
        rrotation = math.radians(rotation)
        # Calculate mid point + rotation offset
        midx = (start_pos[0] + event.x)/2 - math.sin(rrotation)*10
        midy = (start_pos[1] + event.y)/2 - math.cos(rrotation)*10
        # Calculate distance
        dist_num = math.sqrt(
            (start_pos[0] - event.x)**2 + (start_pos[1] - event.y)**2) / universal_scale
        # Calculate distance string
        dist = '{:.0f}ft'.format(dist_num)
        # Create the text
        cur_line_txt = event.widget.create_text(midx, midy, text=dist,
                                                fill="white", font=font.Font(family='Courier New', size=14),
                                                justify=tk.LEFT, angle=rotation)
        # Create the line
        cur_line = event.widget.create_line(start_pos[0], start_pos[1], event.x,
                                            event.y, fill="#3c4048", dash=(3, 5), arrow=tk.BOTH)


def shrink(scale, x=None, y=None):
    global universal_scale
    objs = canvas.find_all()
    for obj in objs:
        if canvas.type(obj) == "text" and not 'scale' in canvas.gettags(obj):
            continue
        if x is None or y is None:
            x = root.winfo_pointerx() - root.winfo_rootx()
            y = root.winfo_pointery() - root.winfo_rooty()
        canvas.scale(obj,x,y,scale,scale)
    universal_scale *= scale


def move(x, y):
    objs = canvas.find_all()
    for obj in objs:
        if canvas.type(obj) == "text" and not 'scale' in canvas.gettags(obj):
            continue
        canvas.move(obj, x, y)

# Function that enables the measuring and saved the initial point


def start_measure(event):
    # print(f'{event.x},{event.y}')
    # Include globals
    global measuring, start_pos, cur_line
    # Save the initial point
    start_pos = (event.x, event.y)
    # Set measuring to True
    measuring = True

def zoom(scale, center=False):
    if center is False:
        shrink(scale)
    else:
        shrink(scale, x=0, y=0)


def stop_measure(event):
    # Include globals
    global measuring, cur_line, cur_line_txt, start_pos
    # Set measuring to False
    measuring = False
    now_pos = (event.x, event.y)
    if start_pos[0] == now_pos[0] and start_pos[1] == now_pos[1]:
        zoom(1.1)
    # Try to remove the old elements
    try:
        event.widget.delete(cur_line)
        event.widget.delete(cur_line_txt)
    except:
        pass


# Bind these functions to motion, press, and release
canvas.bind('<Motion>', measure)
canvas.bind('<Button-1>', start_measure)
canvas.bind('<Button-3>', lambda e: zoom(0.9))
canvas.bind('<Button-2>', lambda e: zoom(0.9))
root.bind('<Up>', lambda e: move(0,move_amt))
root.bind('<Down>', lambda e: move(0,-move_amt))
root.bind('<Left>', lambda e: move(move_amt,0))
root.bind('<Right>', lambda e: move(-move_amt,0))
canvas.bind('<ButtonRelease-1>', stop_measure)

# Include a new create_circle method


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


tk.Canvas.create_circle = _create_circle

def _connect_nodes(self, node1_pos, node2_pos, text=None, dashed=True, color="#3c4048"):
    if node2_pos[0] is None or node2_pos[1] is None or node1_pos[0] is None or node1_pos[1] is None:
        return
    if text is not None:
        # Calculate the rotation between the two points
        rotation = 180 - math.degrees(math.atan2(node1_pos[1] - node2_pos[1],
            node1_pos[0] - node2_pos[0]));
        # node1_pos the rotation
        if rotation > 90 and rotation < 270:
            rotation -= 180
        # Convert to radians
        rrotation = math.radians(rotation)
        # Calculate mid point + rotation offset
        midx = (node1_pos[0] + node2_pos[0])/2 - math.sin(rrotation)*10
        midy = (node1_pos[1] + node2_pos[1])/2 - math.cos(rrotation)*10
        self.create_text(midx, midy, text=text,
            fill="white", font=font.Font(family='Courier New', size=14),
            justify=tk.LEFT,angle=rotation,tag='scale')
    if dashed is True:
        self.create_line(node1_pos[0], node1_pos[1], node2_pos[0], node2_pos[1], fill=color, dash=(3,5))
    else:
        self.create_line(node1_pos[0], node1_pos[1], node2_pos[0], node2_pos[1], fill=color)
tk.Canvas.connect_nodes = _connect_nodes

def _connect_nodes_real(self, node1, node2, text=None, dashed=True, color="#3c4048"):
    node1_pos = node1.get_real_position()
    node2_pos = node2.get_real_position()
    self.connect_nodes(node1_pos, node2_pos, text=text, dashed=dashed, color=color)
tk.Canvas.connect_nodes_real = _connect_nodes_real

def _connect_nodes_guess(self, node1, node2, text=None, dashed=True, color="#3c4048"):
    node1_pos = node1.get_position()
    node2_pos = node2.get_position()
    self.connect_nodes(node1_pos, node2_pos, text=text, dashed=dashed, color=color)
tk.Canvas.connect_nodes_guess = _connect_nodes_guess

def _circle_node(self, node_pos, radius, text, dashed, fill, outline):
    if node_pos[0] is None or node_pos[1] is None:
        return
    if text is not None:
        ypos = node_pos[1]-radius-20
        if ypos < 0:
            ypos = node_pos[1]+radius+20
        self.create_text(node_pos[0],ypos,text=text,
            fill="white", font=font.Font(family='Courier New', size=14),
            justify=tk.LEFT,tag='scale')
    if dashed is True:
        self.create_circle(node_pos[0], node_pos[1], radius, fill=fill, outline=outline,tags=['scale'],dash=(3,5))
    else:
        self.create_circle(node_pos[0], node_pos[1], radius, fill=fill, outline=outline,tags=['scale'])
tk.Canvas.circle_node = _circle_node

def _circle_node_real(self, node, radius, text=None, dashed=True, fill="", outline="red"):
    node_pos = node.get_real_position()
    self.circle_node(node_pos, radius, text, dashed, fill, outline)
tk.Canvas.circle_node_real = _circle_node_real

def _circle_node_guess(self, node, radius, text=None, dashed=True, fill="", outline="red"):
    node_pos = node.get_position()
    self.circle_node(node_pos, radius, text, dashed, fill, outline)
tk.Canvas.circle_node_guess = _circle_node_guess

#
# Import node definitions
#

nodes = {}

with open('./datasets/' + dat_file + '.def', 'r') as defs_file:
    defs_file.readline()
    node_defs = csv.reader(defs_file)
    for node in node_defs:
        if node[2] == '1':  # node.isBase
            nodes[node[0]] = Node(node[0], node[1], True,
                                  float(node[3]), float(node[4]))
        else:
            nodes[node[0]] = Node(node[0], node[1], False,
                                  float(node[3]), float(node[4]))

#
# Import measurements
#

with open('./datasets/' + dat_file + '.dat', 'r') as data_file:
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
    canvas.create_polygon(vals, fill='#2d313c', width=2)

#
# Simulate!
#


def render(nodes, time_taken, note):
    for key, node in nodes.items():
        node.show_real(canvas)
        node.show(canvas)
    root.wm_title(f"Algorithm Result [{alg_name}]")
    t = "%.2fms" % (time_taken*1000)
    l1 = "Algorithm      : {:17s} || # Elements : {:20s}".format(
        alg_name, str(len(nodes)))
    l2 = "Execution Time : {:17s} || # Note     : {:20s}".format(t, note)
    # T.insert(END, f"{l1}\n{l2}\n")
    canvas.create_text(width/2-50, height - 20, text=f"{l1}\n{l2}\n",fill="white", font=font.Font(family='Courier New', size=14),
        justify=tk.RIGHT)
    shrink(width/area_width, x=0, y=0)
    root.mainloop()


algorithm(nodes)._process(render, canvas)
