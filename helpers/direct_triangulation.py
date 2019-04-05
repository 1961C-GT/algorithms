from algorithms.algorithm import Vector2
from algorithms.algorithm import get_intersections
import math


class DirectTriangulation:
    def __init__(self, meas1, meas2, res1=None, res2=None, title=None):
        self.meas1 = meas1
        self.meas2 = meas2
        self.res1 = res1
        self.res2 = res2
        self.title = title
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
            if P0 is not None and P0.y > 100:
                self.guess_list.append(P0)
            if P1 is not None and P1.y > 100:
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


class Cluster:
    def __init__(self, title=None):
        self._points = []
        self.center = None
        self.radius = None
        self.pure = False
        self.title = title

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
