import uuid
import config
from algorithms.helpers.measurement import Measurement
from algorithms.algorithm import Vector2


class Node:
    node_arr = {}
    min_dist = 500    # mm
    max_dist = 1000000 # mm

    def __init__(self, node_id=None, name=None, is_base=False, x=None, y=None, multi_pipe=None):
        if node_id is None:
            node_id = uuid.uuid4()
        if name is None:
            name = ""
        self.id = node_id
        self.name = name
        self.is_base = is_base
        self.real_x = x  # random.randint(25, 600)
        self.real_y = y  # random.randint(25, 600)
        self.resolved = False
        self.triangulate_list = []
        self.multi_pipe = multi_pipe
        self.communicate_list = []
        if self.multi_pipe is not None:
            self.piping = True
        else:
            self.piping = False
        if is_base:
            self.x = x
            self.y = y
            self.resolved = True
        else:
            self.x = None
            self.y = None
        self.measurements = []
        # self.measurement_history = {}

    
    def set_pipe(self, pipe_in):
        self.multi_pipe = pipe_in
        self.piping = True

    def start_new_cycle(self):
        # for other_node in self.communicate_list:
        #     key = other_node.id
        #     if key not in self.measurement_history:
        #         # Add a new list to keep track of measures from this new node
        #         self.measurement_history[key] = []
        #     if self.measurements:
        #         for meas in self.measurements:
        #             if meas.node1 == self:
        #                 self.measurement_history[key].append(meas)
        #     if len(self.measurement_history[key]) > config.MAX_HISTORY:
        #         self.measurement_history[key].pop(0)
        self.measurements = []
        self.triangulate_list = []
        if not self.is_base:
            self.x = None
            self.y = None
            self.resolved = False
        # if self.measurements:
        #     self.measurement_history.append(self.measurements)
        # if len(self.measurement_history) > config.MAX_HISTORY:
        #     self.measurement_history.pop(0)
        # self.measurements = []

    def add_measurement(self, node_b, dist):
        if dist > Node.min_dist and dist < Node.max_dist:
            # print(key)
            # print(self.measurement_history)
            # print(self.measurement_history[key])
            self.measurements.append(Measurement(self, node_b, dist))
            # self.add_to_communicate_list(node_b)
        else:
            # self.measurements.append(Measurement(self, node_b, None))
            # self.add_to_communicate_list(node_b)
            print(f"Discarded meas with {dist} distance to node {node_b.id} due to bounding error.")

    # def add_to_communicate_list(self, node_b):
    #     if node_b not in self.communicate_list:
    #         self.communicate_list.append(node_b)
    #         key = node_b.id
    #         if key not in self.measurement_history:
    #             # Add a new list to keep track of measures from this new node
    #             self.measurement_history[key] = []

    def is_resolved(self):
        return self.resolved

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.resolved = True

    def add_triangulation(self, tri):
        self.triangulate_list.append(tri)

    def get_triangulations(self):
        return self.triangulate_list

    def display_triangulations(self):
        for dt in self.triangulate_list:
            dt.displayTriangulation((self.x, self.y))

    def set_position_vec(self, pos):
        self.x = pos.x
        self.y = pos.y
        self.resolved = True

    def get_position(self):
        return self.x, self.y

    def get_position_vec(self):
        return Vector2(self.x, self.y)

    def get_real_position(self):
        return self.real_x, self.real_y

    def get_real_position_vec(self):
        return Vector2(self.real_x, self.real_y)

    # def error_to_str(self):
    #     if self.x is not None and self.y is not None:
    #         offset = self.get_position_vec() - self.get_real_position_vec()
    #         d = offset.magnitude()
    #         return "{:.3f}ft".format(d)
    #     else:
    #         return "Unresolved"

    # def print_report(self):
    #     if self.x is not None and self.y is not None:
    #         print(str(self), " : ", self.error_to_str() + ' error')

    def get_measurement(self, node_id, history_avg=True):
        # if history_avg:
        #     dist = 0
        #     counter = 0
        #     node2 = None
        #     for meas in self.measurement_history[node_id]:
        #         if meas.dist == None or meas.dist == 0:
        #             continue
        #         node2 = meas.node2
        #         dist = dist + meas.dist
        #         counter = counter + 1
        #     if counter > 0:
        #         dist = dist / counter
        #     else:
        #         return None
        #     return Measurement(self, node2, dist)
        # else:
            return next(filter(lambda m: m.node2.id == node_id, self.measurements))

    def get_measurements(self, history_avg=True):
        # if history_avg:
        #     m = []
        #     for node in self.communicate_list:
        #         key = node.id
        #         dist = 0
        #         counter = 0
        #         for meas in self.measurement_history[key]:
        #             if meas.dist == None or meas.dist == 0:
        #                 continue
        #             dist = dist + meas.dist
        #             counter = counter + 1
        #         if counter > 0:
        #             dist = dist / counter
        #         else:
        #             print("NONE MEAS")
        #         m.append(Measurement(self, node, dist))
        #     # for measurement in self.measurements:
        #     #     m.append(measurement.avg_with_history(self.measurement_history))
        #     return m
        # else:
            return self.measurements

    def clear_measurements(self):
        self.measurements = []

    def show(self):
        if self.x is None or self.y is None or self.multi_pipe is None:
            return
        # fill = "white"
        # if Distance(self.get_real_position_vec(), self.get_position_vec()) < 20:
        #     fill = "green"
        # size = 10
        cmd_obj = {
            "cmd": "draw_circle",
            "args": {
                "fill": "white",
                "r": 1,
                "tags": ['node'],
                "outline": "",
                "x": self.x,
                "y": self.y,
                "convert_to_m": True
            }
        }
        if self.is_base:
            cmd_obj['args']['fill'] = "yellow"
        self.multi_pipe.send(cmd_obj)
        # obj = canvas.create_circle(
        #     self.x, self.y, size, fill=fill, outline="", tags=['node'])
        # if self.real_obj is not None:
        #     coords = canvas.coords(self.real_obj)
        #     x = (coords[0] + coords[2])/2
        #     y = (coords[1] + coords[3])/2
        #     canvas.create_line(self.x, self.y, x, y,
        #                        fill="#3c4048", dash=(3, 5))
        #     canvas.tag_raise(obj)
        #     canvas.tag_raise(self.real_obj)
        # self.guess_obj = obj
        # self.__class__.node_arr[obj] = "#" + str(self.resolution_order) + " | " + str(self) + ' | ' + self.errorToStr()
        # canvas.tag_bind(obj, '<Enter>', self.__class__.nodeEnter)
        # canvas.tag_bind(obj, '<Leave>', self.__class__.nodeLeave)

    def to_string(self):
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

    def __eq__(self, other):
        return self.id == other.id
