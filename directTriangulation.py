from algorithms.algorithm import Algorithm
from algorithms.algorithm import Vector2
from algorithms.algorithm import Intersection
import math
import numpy as np

class DirectTriangulation:
    def __init__(self, meas1, meas2, res1, res2):
        self.meas1 = meas1
        self.meas2 = meas2
        self.res1 = res1
        self.res2 = res2
        self.guess_list = []

    # Triangulate two guesses from the provided measurements
    def triangulate(self):
        if self.meas1 is not None and self.meas2 is not None and self.res1 is not None and self.res2 is not None:
            (P0, P1) = Intersection(res1.get_position_vec(), res2.get_position_vec(), meas1.dist, meas2.dist)
            self.guess_list.append(P0)
            self.guess_list.append(P1)
            # TODO: Remove the guess that is outside the world border

    # Directly add a guess to the guess list, without triangulating it
    def directlyAddGuess(self, guess):
        self.guess_list.append(guess)

    # Get the size of the guess list
    def getNumGuesses(self):
        return len(self.guess_list)

    # Get the guess list
    def getGuesses(self):
        return self.guess_list

    # Get the cloest guess and distance to the provided location
    def getClosestGuess(self, P0):
        if len(self.guess_list) > 0:
            short_dist = math.inf
            return_guess = False
            for guess in self.guess_list:
                offset = P0 - guess
                d = offset.magnitude()
                if d < short_dist:
                    short_dist = d
                    return_guess = guess
            return (return_guess, short_dist)
        else:
            return False


class Cluster:
    def __init__(self, title=None):
        self._points = []
        self.center = None
        self.radius = None
        self.pure = False
        self.title = title

    # Add a point to the cluster
    def addPoint(self, point):
        self._points.append(point)
        self.pure = False

    def addPoints(self, points_arr):
        self._points = self._points + points_arr
        self.pure = False

    # Get the points from the cluster
    def getPoints(self):
        return self._points

    # Get the center of the cluster
    def getCenter(self):
        if self.center is None or self.pure is False:
            length = len(self._points)
            sum_x = 0
            sum_y = 0
            for p in self._points:
                sum_x += p.x
                sum_y += p.y
            self.center = Vector2(sum_x/length, sum_y/length)
            self.pure = True
            self.radius = None
        return self.center

    # Get the radius of the cluster
    def getRadius(self):
        if self.radius is None or self.pure is False:
            center = self.getCenter()
            self.radius = 0
            for p in self._points:
                offset = p - center
                d = offset.magnitude()
                if d > self.radius:
                    self.radius = d
        return self.radius
        
    # Display the cluster on the UI
    def display(self, canvas):
        if self.pure is False:
            self.getRadius()
        for p in self._points:
            canvas.circle_area(p.x, p.y, 2, dashed=False, outline="", fill="red")
        canvas.circle_area(self.center.x, self.center.y, self.radius, outline="#375772", text=self.title)
