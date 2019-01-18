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
move_amt = 20

print("Data File: " + sys.argv[1])
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
root.resizable(width=False, height=False)
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


def shrink(scale):
    global universal_scale
    objs = canvas.find_all()
    for obj in objs:
        if canvas.type(obj) == "text":
            continue
        x = root.winfo_pointerx()
        y = root.winfo_pointery()
        abs_coord_x = root.winfo_pointerx() - root.winfo_rootx()
        abs_coord_y = root.winfo_pointery() - root.winfo_rooty()
        canvas.scale(obj, abs_coord_x, abs_coord_y, scale, scale)
    universal_scale *= scale


def move(x, y):
    objs = canvas.find_all()
    for obj in objs:
        if canvas.type(obj) == "text":
            continue
        canvas.move(obj, x, y)

# Function that enables the measuring and saved the initial point


def start_measure(event):
    # Include globals
    global measuring, start_pos, cur_line
    # Save the initial point
    start_pos = (event.x, event.y)
    # Set measuring to True
    measuring = True


def zoom_in(event):
    shrink(0.9)


def stop_measure(event):
    # Include globals
    global measuring, cur_line, cur_line_txt, start_pos
    # Set measuring to False
    measuring = False
    now_pos = (event.x, event.y)
    if start_pos[0] == now_pos[0] and start_pos[1] == now_pos[1]:
        shrink(1.1)
    # Try to remove the old elements
    try:
        event.widget.delete(cur_line)
        event.widget.delete(cur_line_txt)
    except:
        pass


# Bind these functions to motion, press, and release
canvas.bind('<Motion>', measure)
canvas.bind('<Button-1>', start_measure)
canvas.bind('<Button-3>', zoom_in)
canvas.bind('<Button-2>', zoom_in)
root.bind('<Up>', lambda e: move(0, -move_amt))
root.bind('<Down>', lambda e: move(0, move_amt))
root.bind('<Left>', lambda e: move(-move_amt, 0))
root.bind('<Right>', lambda e: move(move_amt, 0))
canvas.bind('<ButtonRelease-1>', stop_measure)

# Init the text field at the bottom of the simulator
# T = Text(root, height=2, font = font.Font(family='Courier New', size=14))
# T.grid(column=0,row=1)

# Include a new create_circle method


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(10*x-r, 10*y-r, 10*x+r, 10*y+r, **kwargs)


tk.Canvas.create_circle = _create_circle

#
# Import node definitions
#

nodes = {}

with open('./datasets/' + sys.argv[1] + '.def', 'r') as defs_file:
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

with open('./datasets/' + sys.argv[1] + '.dat', 'r') as data_file:
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
    l1 = "Algorithm      : {:17s} || # Elements : {:20s}".format(
        sys.argv[2], str(len(nodes)))
    l2 = "Execution Time : {:17s} || # Note     : {:20s}".format(t, note)
    # T.insert(END, f"{l1}\n{l2}\n")
    canvas.create_text(width/2-50, height - 20, text=f"{l1}\n{l2}\n", fill="white", font=font.Font(family='Courier New', size=14),
                       justify=tk.RIGHT)

    root.mainloop()


algorithm(nodes)._process(render, canvas)
