import time
import math
import builtins as __builtin__


class Algorithm:
    old_print = print
    time_only = True

    def __init__(self, nodes):
        self.nodes = nodes
        self.start = 0
        self.end = 0
        self.note = 'None'

    @staticmethod
    def class_print(*args, **kwargs):
        """My custom print() function."""
        # Adding new arguments to the print function signature
        # is probably a bad idea.
        # Instead consider testing if custom argument keywords
        # are present in kwargs
        t = '{0:.2f}'.format((time.time() - __class__.__stime__) * 1000)
        if __class__.time_only is True:
            __class__.old_print('{:14s}'.format(f'[{t}ms] '), end='')
        else:
            __class__.old_print('{:30s}'.format(f'[{__class__.__cname__} | {t}ms] '), end='')
        return __class__.old_print(*args, **kwargs)

    def _process(self, callback):
        global print
        self._callback = callback
        print(
            '\n##########################################################################')
        print(f'Start Algorithm Process [{self.__class__.__name__}]')
        print('##########################################################################')
        __class__.__cname__ = self.__class__.__name__
        old_print = __builtin__.print
        __builtin__.print = self.__class__.class_print
        self.start = time.time()
        __class__.__stime__ = self.start
        self.process(self._run_callback)

    def _run_callback(self, render=True):
        global print
        self.end = time.time()
        __builtin__.print = self.__class__.old_print
        print(
            '##########################################################################\n')
        print("Algorithm time: %.2fms" % ((self.end - self.start) * 1000))
        if render is True:
            self._callback(self.nodes, self.end - self.start, self.note)

    def process(self, callback):
        pass

    def _type(self):
        return self.__class__.__name__


def get_distance(p0, p1):
    if p0.x is None or p0.y is None or p1.x is None or p1.y is None:
        return math.inf
    offset = p1 - p0
    return offset.magnitude()


# Determines whether two circles collide and, if applicable,
# the points at which their borders intersect.
# Based on an algorithm described by Paul Bourke:
# https://web.archive.org/web/20060911063359/http://local.wasp.uwa.edu.au/~pbourke/geometry/2circle/
# Arguments:
#   P0 (Vector2): the centre point of the first circle
#   P1 (Vector2): the centre point of the second circle
#   r0 (number): radius of the first circle
#   r1 (number): radius of the second circle
# Returns:
#   False if the circles do not collide
#   True if one circle wholly contains another such that the borders
#       do not overlap, or overlap exactly (e.g. two identical circles)
#   An array of two vectors containing the intersection points
#       if the circle's borders intersect.
def get_intersections(p0, p1, r0, r1):
    if type(p0) != Vector2 or type(p1) != Vector2:
        raise TypeError("p0 and p1 must be vectors")

    # equation 1
    offset = p1 - p0
    d = offset.magnitude()

    # equation 2: simple cases
    if d > (r0 + r1):
        # no collision
        return [None, None]
    elif d == 0 or d < abs(r0 - r1):
        # full containment
        return [None, None]

    # equation 3
    a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)

    # equation 4
    h = math.sqrt(r0 ** 2 - a ** 2)

    # equation 5
    p2 = p0 + a * (p1 - p0) / d

    # equation 6
    if d == r0 + r1:
        return [p2, None]

    # equation 8
    alpha_x = p2.x + h * (p1.y - p0.y) / d
    alpha_y = p2.y - h * (p1.x - p0.x) / d
    alpha = Vector2(alpha_x, alpha_y)

    # equation 9
    beta_x = p2.x - h * (p1.y - p0.y) / d
    beta_y = p2.y + h * (p1.x - p0.x) / d
    beta = Vector2(beta_x, beta_y)

    return [alpha, beta]


# Simple 2D vector class.
# Based on work by @mcleonard on github:
# https://gist.github.com/mcleonard/5351452
class Vector2(object):
    def __init__(self, x, y):
        """Create a vector, e.g. v = Vector2(10, 15)"""
        self.x = x
        self.y = y

    def magnitude(self):
        """Returns the magnitude of this vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        """Returns the vector addition of self and other."""
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Returns the vector difference of self and other."""
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Multiplies each component if other is a scalar"""
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        """Divides each component if other is a scalar"""
        return Vector2(self.x / other, self.y / other)

    def __truediv__(self, other):
        """Divides each component if other is a scalar"""
        return Vector2(self.x / other, self.y / other)

    def __str__(self):
        """Returns this vector as a string of the form: (x, y)"""
        return "(%(x)d, %(y)d)" % {"x": self.x, "y": self.y}
