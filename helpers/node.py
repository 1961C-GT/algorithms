import uuid
import config
from algorithms.helpers.measurement import Measurement
from algorithms.algorithm import Vector2
from algorithms.helpers.direct_triangulation import DirectTriangulation


class Node:
    node_arr = {}
    min_dist = 500    # mm
    max_dist = 1000000 # mm
    max_history = 10
    max_move_per_cycle = 5000

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
        self.measurements = []
        self.triangulate_list = []
        if not self.is_base:
            self.x = None
            self.y = None
            self.resolved = False
        self.extrapolate = False

        if self.added_position is False:
            if len(self.position_history) > 0:
                self.position_history.pop(0)

        self.added_position = False
        # if self.measurements:
        #     self.measurement_history.append(self.measurements)
        # if len(self.measurement_history) > config.MAX_HISTORY:
        #     self.measurement_history.pop(0)
        # self.measurements = []

    def add_measurement(self, node_b, dist, std=None):
        if dist > Node.min_dist and dist < Node.max_dist:
            # print(key)
            # print(self.measurement_history)
            # print(self.measurement_history[key])
            self.measurements.append(Measurement(self, node_b, dist, std=std))
            # self.add_to_communicate_list(node_b)
        else:
            # self.measurements.append(Measurement(self, node_b, None))
            # self.add_to_communicate_list(node_b)
            print(f"Discarded meas with {dist} distance to node {node_b.id} due to bounding error.")

    def is_resolved(self):
        return self.resolved


    def get_last_position(self):
        if len(self.position_history) == 0:
            return None
        return self.position_history[len(self.position_history)-1]
    
    def get_avg_position(self):
        x_sum = 0
        y_sum = 0
        counter = 0
        for pos in self.position_history:
            x_sum += pos[0]
            y_sum += pos[1]
            counter += 1
        return (x_sum/counter, y_sum/counter)
    
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
        # last = self.get_last_position()
        # if last is None:
        #     last_pos = pos
        # else:
        #     last_pos = Vector2(last[0], last[1])
        # offset = last_pos - pos
        # d = offset.magnitude()

        # print(d)

        # if d <= Node.max_move_per_cycle:
        self.x = pos.x
        self.y = pos.y
        # else:
            # vel = self.get_avg_velocity()
            # pos = Vector2(last[0], last[1])
            # new_pos = pos + vel
            # self.x = new_pos.x
            # self.y = new_pos.y
            # self.extrapolate = True
        
        self.position_history.append((pos.x, pos.y))
        self.added_position = True
        if len(self.position_history) > Node.max_history:
            self.position_history.pop(0)

        self.resolved = True

    def consider_last_location(self):
        last = self.get_last_position()
        if last is not None:
            dt = DirectTriangulation(None, None, None, None, empty=True)
            dt.directly_add_guess(Vector2(last[0], last[1]))
            self.add_triangulation(dt)

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
                "r": 200,
                "tags": ['node'],
                "outline": "",
                "x": self.x,
                "y": self.y,
                "convert_to_m": True
            }
        }
        if self.is_base:
            cmd_obj['args']['fill'] = "yellow"

        if self.extrapolate:
            cmd_obj['args']['fill'] = "purple"

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
