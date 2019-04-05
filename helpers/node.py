import uuid
import config
from algorithms.helpers.measurement import Measurement
from algorithms.algorithm import Vector2


class Node:
    node_arr = {}

    def __init__(self, node_id=None, name=None, is_base=False, x=None, y=None):
        if node_id is None:
            node_id = uuid.uuid4()
        if name is None:
            name = ""
        self.id = node_id
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
        self.measurement_history = []

    def start_new_cycle(self):
        if self.measurements:
            self.measurement_history.append(self.measurements)
        if len(self.measurement_history) > config.MAX_HISTORY:
            self.measurement_history.pop(0)
        self.measurements = []

    def add_measurement(self, node_b, dist):
        self.measurements.append(Measurement(self, node_b, dist))

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

    def error_to_str(self):
        if self.x is not None and self.y is not None:
            offset = self.get_position_vec() - self.get_real_position_vec()
            d = offset.magnitude()
            return "{:.3f}ft".format(d)
        else:
            return "Unresolved"

    def print_report(self):
        if self.x is not None and self.y is not None:
            print(str(self), " : ", self.error_to_str() + ' error')

    def get_measurement(self, node_id):
        return next(filter(lambda m: m.node2.id == node_id, self.measurements))

    def get_measurements(self):
        return self.measurements

    def clear_measurements(self):
        self.measurements = []

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
