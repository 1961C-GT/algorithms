import uuid

from algorithms.helpers.measurement import Measurement
from algorithms.algorithm import Vector2
from algorithms.helpers.direct_triangulation import DirectTriangulation


class Node:
    node_arr = {}
    min_dist = 500  # mm
    max_dist = 1000000  # mm
    max_history = 10
    max_move_per_cycle = 5000
    use_s_last = True

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
        self.guess_radius = -1
        self.resolved = False
        self.extrapolate = False
        self.triangulate_list = []
        self.multi_pipe = multi_pipe
        self.communicate_list = []
        self.position_history = []
        self.added_position = False
        if self.multi_pipe is not None:
            self.piping = True
        else:
            self.piping = False
        if is_base:
            if x is None:
                x = 0
            if y is None:
                y = 0
            self.x = x
            self.y = y
            self.resolved = True
        else:
            self.x = None
            self.y = None
        self.measurements = []
        # self.measurement_history = {}

    def force_set_resolved(self, resolved):
        self.resolved = resolved

    def set_real_x_pos(self, x):
        self.real_x = x
        self.x = x
        self.resolved = True

    def set_pipe(self, pipe_in):
        self.multi_pipe = pipe_in
        self.piping = True

    def start_new_cycle(self):
        self.measurements = []
        self.triangulate_list = []
        self.guess_radius = -1
        if not self.is_base:
            self.x = None
            self.y = None
            self.resolved = False
        self.extrapolate = False

        if self.added_position is False:
            if len(self.position_history) > 0:
                self.position_history.pop(0)

        self.added_position = False

    def add_measurement(self, node_b, dist, std=None):
        if Node.min_dist < dist < Node.max_dist:
            self.measurements.append(Measurement(self, node_b, dist, std=std))
        else:
            print(f"Discarded meas with {dist} distance to node {node_b.id} due to bounding error.")

    def is_resolved(self):
        return self.resolved

    def set_solving_cluster(self, cluster):
        self.guess_radius = cluster.get_radius()

    def get_guess_radius(self):
        return self.guess_radius

    def get_last_position(self):
        if len(self.position_history) == 0:
            return None
        return self.position_history[len(self.position_history) - 1]

    def get_second_last_position(self):
        if len(self.position_history) < 2:
            return None
        return self.position_history[len(self.position_history) - 2]

    def get_avg_position(self):
        x_sum = 0
        y_sum = 0
        counter = 0
        for pos in self.position_history:
            x_sum += pos[0]
            y_sum += pos[1]
            counter += 1
        return x_sum / counter, y_sum / counter

    def get_avg_velocity(self):
        hist_vec = []
        for pos in self.position_history:
            hist_vec.append(Vector2(pos[0], pos[1]))
        vec_sum = Vector2(0, 0)
        for pos in hist_vec:
            vec_sum = vec_sum + pos
        return vec_sum / len(hist_vec)

    def add_triangulation(self, tri):
        self.triangulate_list.append(tri)

    def get_triangulations(self):
        return self.triangulate_list

    def display_triangulations(self):
        for dt in self.triangulate_list:
            dt.display_triangulation((self.x, self.y))

    def set_position_vec(self, pos):
        self.x = pos.x
        self.y = pos.y

        self.position_history.append((pos.x, pos.y))
        self.added_position = True
        if len(self.position_history) > Node.max_history:
            self.position_history.pop(0)

        self.resolved = True

    def consider_last_location(self):
        last = self.get_last_position()
        slast = self.get_second_last_position()
        if last is not None:
            dt = DirectTriangulation(None, None, None, None, empty=True)
            dt.directly_add_guess(Vector2(last[0], last[1]))
            self.add_triangulation(dt)
        if Node.use_s_last and slast is not None:
            dt = DirectTriangulation(None, None, None, None, empty=True)
            dt.directly_add_guess(Vector2(slast[0], slast[1]))
            self.add_triangulation(dt)

    def get_position(self):
        return self.x, self.y

    def get_position_vec(self):
        return Vector2(self.x, self.y)

    def get_real_position(self):
        return self.real_x, self.real_y

    def get_real_position_vec(self):
        return Vector2(self.real_x, self.real_y)

    def get_measurement(self, node_id, history_avg=True):
        return next(filter(lambda m: m.node2.id == node_id, self.measurements))

    def get_measurements(self, history_avg=True):
        return self.measurements

    def clear_measurements(self):
        self.measurements = []

    def show(self):
        if self.x is None or self.y is None or self.multi_pipe is None or self.resolved is False:
            return
        cmd_obj = {
            "cmd": "draw_circle",
            "args": {
                "fill": "text",
                "r": 200,
                "tags": ['node'],
                "outline": "blank",
                "x": self.x,
                "y": self.y,
                "convert_to_m": True,
                "text": self.name,
                "text_color": "text",
                "text_size": "text_size_small"
            }
        }
        if self.is_base:
            cmd_obj['args']['fill'] = "yellow"
            cmd_obj['args']['text_size'] = 14
            cmd_obj['args']['text_y_bias'] = -20
        else:
            for hist in self.position_history:
                h = {
                    "cmd": "draw_circle",
                    "args": {
                        "fill": "grey",
                        "r": 100,
                        "tags": ['node'],
                        "outline": "blank",
                        "x": hist[0],
                        "y": hist[1],
                        "convert_to_m": True
                    }
                }
                self.multi_pipe.send(h)

        if self.extrapolate:
            cmd_obj['args']['fill'] = "purple"

        self.multi_pipe.send(cmd_obj)

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
