from algorithms.algorithm import Vector2
from algorithms.algorithm import get_intersections
import math


class DirectTriangulation:
    def __init__(self, meas1, meas2, res1=None, res2=None, empty=False, title=None, multi_pipe=None):
        self.meas1 = meas1
        self.meas2 = meas2
        self.res1 = res1
        self.res2 = res2
        self.title = title
        self.multi_pipe = multi_pipe
        if empty is False:
            if self.res1 is None:
                self.res1 = self.meas1.get_resolved_node()
            if self.res2 is None:
                self.res2 = self.meas2.get_resolved_node()
            if self.res1 is None or self.res1 is False or self.res2 is None or self.res2 is False:
                print("---ERROR--- Both measurements require a resolved node, or resolved nodes must be provided.")
                return
        self.guess_list = []

    # Triangulate two guesses from the provided measurements
    def triangulate(self):
        if self.meas1 is not None and self.meas2 is not None and self.res1 is not None and self.res2 is not None:
            (P0, P1) = get_intersections(self.res1.get_position_vec(), self.res2.get_position_vec(), self.meas1.dist,
                                         self.meas2.dist)
            # TODO: Remove the guess that is outside the world border / make it better
            if P0 is not None and P0.y > 0:
                self.guess_list.append(P0)
            if P1 is not None and P1.y > 0:
                self.guess_list.append(P1)

    # Directly add a guess to the guess list, without triangulating it
    def directly_add_guess(self, guess):
        self.guess_list.append(guess)

    # Get the size of the guess list
    def get_num_guesses(self):
        return len(self.guess_list)

    # Get the guess list
    def get_guesses(self):
        return self.guess_list

    # Get the cloest guess and distance to the provided location
    def get_closest_guess(self, p0):
        if len(self.guess_list) > 0:
            short_dist = math.inf
            return_guess = False
            for guess in self.guess_list:
                offset = p0 - guess
                d = offset.magnitude()
                if d < short_dist:
                    short_dist = d
                    return_guess = guess
            return return_guess, short_dist
        else:
            return None, None

    def display(self):
        # print("dt display")
        if self.multi_pipe is None:
            return
        for guess in self.guess_list:
            self.multi_pipe.send({
                "cmd": "draw_circle",
                "args": {
                    "x": guess.x,
                    "y": guess.y,
                    "r": 150,
                    "dashed": False,
                    "outline": "blank",
                    "fill": "guess"
                }
            })

    def display_triangulation(self, resolved_position):
        # print("dt displayTriangulation")
        if self.multi_pipe is None:
            return
        d1 = ((Vector2(resolved_position[0], resolved_position[1]) - self.res1).magnitude()) / 1000
        d2 = ((Vector2(resolved_position[0], resolved_position[1]) - self.res2).magnitude()) / 1000

        for guess in self.guess_list:
            self.multi_pipe.send({
                "cmd": "connect_points",
                "args": {
                    "pos1": (guess.x, guess.y),
                    "pos2": (self.res1.x, self.res1.y),
                    "dashed": True,
                    "color": "ghost_line"
                }
            })
            self.multi_pipe.send({
                "cmd": "connect_points",
                "args": {
                    "pos1": (guess.x, guess.y),
                    "pos2": (self.res2.x, self.res2.y),
                    "dashed": True,
                    "color": "ghost_line"
                }
            })
        self.multi_pipe.send({
            "cmd": "connect_points",
            "args": {
                "pos1": resolved_position,
                "pos2": (self.res1.x, self.res1.y),
                "dashed": True,
                "color": "highlight_line",
                "text": str(round(d1)) + "m",
                "text_size": "text_size_small",
                "text_color": "highlight_line"
            }
        })
        self.multi_pipe.send({
            "cmd": "connect_points",
            "args": {
                "pos1": resolved_position,
                "pos2": (self.res2.x, self.res2.y),
                "dashed": True,
                "color": "highlight_line",
                "text": str(round(d2)) + "m",
                "text_size": "text_size_small",
                "text_color": "highlight_line"
            }
        })


class Cluster:
    def __init__(self, title=None, multi_pipe=None):
        self._points = []
        self.center = None
        self.radius = None
        self.pure = False
        self.title = title
        self.multi_pipe = multi_pipe

    # Add a point to the cluster
    def add_point(self, point):
        self._points.append(point)
        self.pure = False

    def add_points(self, points_arr):
        self._points = self._points + points_arr
        self.pure = False

    # Get the points from the cluster
    def get_points(self):
        return self._points

    # Get the number of points in the cluster
    def get_num_points(self):
        return len(self._points)

    # Get the center of the cluster
    def get_center(self):
        if self.center is None or self.pure is False:
            length = len(self._points)
            sum_x = 0
            sum_y = 0
            for p in self._points:
                sum_x += p.x
                sum_y += p.y
            self.center = Vector2(sum_x / length, sum_y / length)
            self.pure = True
            self.radius = None
        return self.center

    # Get the radius of the cluster
    def get_radius(self):
        if self.radius is None or self.pure is False:
            center = self.get_center()
            self.radius = 0
            for p in self._points:
                offset = p - center
                d = offset.magnitude()
                if d > self.radius:
                    self.radius = d
        return self.radius

    # Display the cluster on the UI
    def display(self, ghost=False):
        if self.multi_pipe is None:
            return
        if self.pure is False:
            self.getRadius()
        for p in self._points:
            point_obj = {
                "cmd": "draw_circle",
                "args": {
                    "x": p.x,
                    "y": p.y,
                    "r": 100,
                    "dashed": False,
                    "outline": "blank",
                    "fill": "guess"
                }
            }
            if ghost is True:
                # point_obj['args']['fill'] = "#4678a1"
                point_obj['args']['fill'] = "orange"
            self.multi_pipe.send(point_obj)
        main_obj = {
            "cmd": "draw_circle",
            "args": {
                "x": self.center.x,
                "y": self.center.y,
                "r": self.radius,
                "dashed": True,
                "outline": "ghost_line",
                "fill": "blank",
                "width": 1
            }
        }
        if ghost is False:
            main_obj['args']['outline'] = "ghost_line_blue"
        self.multi_pipe.send(main_obj)
