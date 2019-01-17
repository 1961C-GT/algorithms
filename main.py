import sys
import importlib
import tkinter as tk
from node import Node
from measure import Measurement

print("Simulation Start: " + sys.argv[1])

module = importlib.import_module('Algorithms.' + sys.argv[1] + '.' + sys.argv[1])

root = tk.Tk()
canvas = tk.Canvas(root, width=650, height=650, borderwidth=0, highlightthickness=0, bg="black")
canvas.grid()
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

# Simulation Code Init ############

node_arr = {
    'A1': Node('A1', base=True),
    'A2': Node('A2', base=True),
    'B': Node('B'),
    'C1': Node('C1'),
    'C2': Node('C2'),
    'C3': Node('C3'),
    'C4': Node('C4'),
    'C5': Node('C5'),
    'C6': Node('C6'),
    'C7': Node('C7')
}

node_arr['A1'].addMeasurement(node_arr['A2'], 21.625)
node_arr['A1'].addMeasurement(node_arr['B'], 16.5)
node_arr['A1'].addMeasurement(node_arr['C1'], 13.25)
node_arr['A1'].addMeasurement(node_arr['C2'], 12.375)
node_arr['A1'].addMeasurement(node_arr['C3'], 12.25)
node_arr['A1'].addMeasurement(node_arr['C4'], 13.875)
node_arr['A1'].addMeasurement(node_arr['C5'], 12.625)
node_arr['A1'].addMeasurement(node_arr['C6'], 16.75)
node_arr['A1'].addMeasurement(node_arr['C7'], 23.75)
node_arr['A2'].addMeasurement(node_arr['B'], 19.75)
node_arr['A2'].addMeasurement(node_arr['C1'], 15)
node_arr['A2'].addMeasurement(node_arr['C2'], 15.125)
node_arr['A2'].addMeasurement(node_arr['C3'], 13.75)
node_arr['A2'].addMeasurement(node_arr['C4'], 13.875)
node_arr['A2'].addMeasurement(node_arr['C5'], 12.875)
node_arr['A2'].addMeasurement(node_arr['C6'], 13.125)
node_arr['A2'].addMeasurement(node_arr['C7'], 23.25)
node_arr['B'].addMeasurement(node_arr['C1'], 5.625)
node_arr['B'].addMeasurement(node_arr['C2'], 6.125)
node_arr['B'].addMeasurement(node_arr['C3'], 7.375)
node_arr['B'].addMeasurement(node_arr['C4'], 6.375)
node_arr['B'].addMeasurement(node_arr['C5'], 7.625)
node_arr['B'].addMeasurement(node_arr['C6'], 6.75)
node_arr['B'].addMeasurement(node_arr['C7'], 7.375)
node_arr['C1'].addMeasurement(node_arr['C2'], 0.875)
node_arr['C1'].addMeasurement(node_arr['C3'], 1.7188)
node_arr['C1'].addMeasurement(node_arr['C4'], 1.1875)
node_arr['C1'].addMeasurement(node_arr['C5'], 2.1562)
node_arr['C1'].addMeasurement(node_arr['C6'], 4)
node_arr['C1'].addMeasurement(node_arr['C7'], 11.9375)
node_arr['C2'].addMeasurement(node_arr['C3'], 1.375)
node_arr['C2'].addMeasurement(node_arr['C4'], 1.75)
node_arr['C2'].addMeasurement(node_arr['C5'], 2.2812)
node_arr['C2'].addMeasurement(node_arr['C6'], 4.7188)
node_arr['C2'].addMeasurement(node_arr['C7'], 12.75)
node_arr['C3'].addMeasurement(node_arr['C4'], 1.625)
node_arr['C3'].addMeasurement(node_arr['C5'], 1.1875)
node_arr['C3'].addMeasurement(node_arr['C6'], 4.4688)
node_arr['C3'].addMeasurement(node_arr['C7'], 13.5)
node_arr['C4'].addMeasurement(node_arr['C5'], 1.25)
node_arr['C4'].addMeasurement(node_arr['C6'], 3)
node_arr['C4'].addMeasurement(node_arr['C7'], 12)
node_arr['C5'].addMeasurement(node_arr['C6'], 3.4375)
node_arr['C5'].addMeasurement(node_arr['C7'], 13.25)
node_arr['C6'].addMeasurement(node_arr['C7'], 10.9375)


# Simulation Code Calc ############


class_ = getattr(module, sys.argv[1])
instance = class_(node_arr)

def render(node_arr):
    for key,node in node_arr.items():
        node.show(canvas)
    root.wm_title("Circles and Arcs")
    root.mainloop()

instance._process(render)
