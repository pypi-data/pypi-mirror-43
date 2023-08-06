import cmath
import copy
from math import atan, cos, sin, pi

from PIL import Image, ImageDraw

"""
A lib to draw fractals on pillow image

>>> img = Image.new('RGB', (5000, 5000), (0, 0, 0))
>>> figures = Figures(im=img)
>>> figures.von_koch_curve_flake((2500, 2500), 2000,6)
>>> img.save("test.bmp")
"""


class State:
    """State of Lsystem"""
    width: int
    color: tuple
    angle: int
    y: int
    x: int

    def __init__(self):
        """Initialisation of state

        >>> State().x
        0
        >>> State().y
        0
        >>> State().angle
        0
        >>> State().color
        (255, 255, 255)
        >>> State().width
        0"""
        self.x = 0
        self.y = 0
        self.angle = 0
        self.color = (255, 255, 255)
        self.width = 0

    def __str__(self):
        return str(self.x)

    def __repr__(self):
        return self.__str__()


class Lsystem(ImageDraw.ImageDraw):
    """Draw a L system"""
    state: State
    states: list

    def dragon(self, size, recursions, color=None, width=0):
        """Trace Dragon curve

        :param size: Lenght of a segment
        :param recursions: number of recursions
        :param color: color of drawing
        :param width: width of drawing
        :type size: float
        :type recursions: int
        :type color: tuple
        :type width: int"""
        self.draw_l("FX",
                    {"X": "X+YF+",
                     "Y": "-FX-Y"},
                    {"-": self.left(pi / 2),
                     '+': self.right(pi / 2),
                     "F": self.forward(size),
                     "Y": self.nothing(),
                     "X": self.nothing()},
                    recursions,
                    color, width)

    def sierpinski_triangle(self, size, recursions, color=None, width=0):
        """Draw the sierpinski triangle

        :param size: Lenght of a segment
        :param recursions: number of recursions
        :param color: color of drawing
        :param width: width of drawing
        :type size: float
        :type recursions: int
        :type color: tuple
        :type width: int"""
        self.draw_l("F-G-G",
                    {"F": "F-G+F+G-F",
                     "G": "GG"},
                    {"-": self.left(pi * 2 / 3),
                     '+': self.right(pi * 2 / 3),
                     "F": self.forward(size),
                     "G": self.forward(size)},
                    recursions,
                    color, width)

    def fractal_plant(self, size, recursions, color=None, width=0):
        """Draw the fractal plant

        :param size: Lenght of a segment
        :param recursions: number of recursions
        :param color: color of drawing
        :param width: width of drawing
        :type size: float
        :type recursions: int
        :type color: tuple
        :type width: int"""
        self.draw_l("X",
                    {"X": "F+[[X]-X]-F[-FX]+X",
                     "F": "FF"},
                    {"-": self.left(pi * 5 / 36),
                     '+': self.right(pi * 5 / 36),
                     "F": self.forward(size),
                     "X": self.nothing(),
                     "[": self.save(),
                     "]": self.restore()},
                    recursions,
                    color, width)

    def koch_curve_right_angle(self, size, recursions, color=None, width=0):
        """Draw koch curve with right angle

        :param size: Lenght of a segment
        :param recursions: number of recursions
        :param color: color of drawing
        :param width: width of drawing
        :type size: float
        :type recursions: int
        :type color: tuple
        :type width: int"""
        self.draw_l("F",
                    {"F": "F+F-F-F+F"},
                    {"-": self.left(pi / 2),
                     '+': self.right(pi / 2),
                     "F": self.forward(size),
                     "[": self.save(),
                     "]": self.restore()},
                    recursions,
                    color, width)

    def fractal_binary_tree(self, size, recursions, color=None, width=0):
        """Draw fractal binary tree

        :param size: Lenght of a segment
        :param recursions: number of recursions
        :param color: color of drawing
        :param width: width of drawing
        :type size: float
        :type recursions: int
        :type color: tuple
        :type width: int"""
        self.draw_l("0",
                    {"1": "11",
                     "0": "1[-0]+0"},
                    {"-": self.left(pi / 2),
                     '+': self.right(pi / 2),
                     "0": self.forward(size),
                     "1": self.forward(size),
                     "[": self.save(),
                     "]": self.restore()},
                    recursions,
                    color, width)

    def __init__(self, *args, **kwargs):
        """Initialisation

        Parameters are the same than ImageDraw.__init__"""
        super().__init__(*args, **kwargs)
        self.states = []
        self.state = State()

    def set_pos(self, x, y):
        """Set position of pen

        :param x: x coordinate
        :param y: y coordinate
        :type x: float
        :type y: float"""

        self.state.x = x
        self.state.y = y

    def _right(self, angle):
        """Turn pen to right of angle

        :param angle: Angle to rotate
        :type angle: float
        """
        self.state.angle -= angle

    def _left(self, angle):
        """Turn pen to left of angle

        :param angle: Angle to rotate
        :type angle: float
        """
        self.state.angle += angle

    def _forward(self, distance):
        """Forward pen of distance

        :param distance: Distance to forward
        :type distance: float
        """
        x_2: float = (distance * cos(self.state.angle)) + self.state.x
        y_2: float = (distance * sin(self.state.angle)) + self.state.y
        self.line(((self.state.x, self.state.y), (x_2, y_2)), self.state.color, self.state.width)
        self.state.x, self.state.y = x_2, y_2

    def _backward(self, distance):
        """Backward pen of distance

        :param distance: Distance to backward
        :type distance: float
        """
        self._forward(-distance)

    def _save(self):
        """Save state of pen"""
        self.states.append(copy.deepcopy(self.state))

    def _restore(self):
        """Restore last pen state"""
        self.state = self.states.pop()

    def draw_l(self, start, replacement, constants, nb_recursive, color=(255, 255, 255), width=0):
        """Draw a L system

        :param start: Axiome
        :param replacement: Dictionary which contain replacement values (F->F+F-F-F+F)
        :param constants: Dictionary which contain all elements with there function
        :param nb_recursive: Number of recursion
        :param color: Color to use for the drawing
        :param width: The line width, in pixels
        :type start: str
        :type replacement: dict
        :type constants: dict
        :type nb_recursive: int
        :type color: tuple
        :type width: int
        """
        self.state.color = color
        self.state.width = width
        for i in range(nb_recursive):
            newstart = ""
            for carac in start:
                if carac in replacement:
                    newstart += replacement[carac]
                else:
                    newstart += carac
            start = newstart
        for item in start:
            constants[item]()

    def right(self, angle):
        """Return a lambda function which make pen turning of angle radians to right

        :param angle: Angle to build function
        :type angle: float

        :return: lambda function to make pen turning right
        :rtype: lambda"""
        return lambda: self._right(angle)

    def left(self, angle):
        """Return a lambda function which make pen turning of angle radians to left

        :param angle: Angle to build function
        :type angle: float

        :return: lambda function to make pen turning left
        :rtype: lambda"""
        return lambda: self._left(angle)

    def forward(self, distance):
        """Return a lambda function which make pen forward of distance

        :param distance: Distance to build function
        :type distance: float

        :return: lambda function to make pen forward
        :rtype: lambda"""
        return lambda: self._forward(distance)

    def backward(self, distance):
        """Return a lambda function which make pen backward of distance

        :param distance: Distance to build function
        :type distance: float

        :return: lambda function to make pen backward
        :rtype: lambda"""
        return lambda: self._backward(distance)

    def save(self):
        """Return a lambda function which save state of pen

        :return: lambda function to save pen state
        :rtype: lambda"""
        return lambda: self._save()

    def restore(self):
        """Return a lambda function which restore state of pen

        :return: lambda function to restore pen state
        :rtype: lambda"""
        return lambda: self._restore()

    def nothing(self):
        return lambda: None


class Figures(ImageDraw.ImageDraw):
    """A lot of function to create some well-know shapes"""

    @staticmethod
    def point_to_complex(point):
        """Transform tuple to complex

        :param point: Point to convert
        :type point: tuple

        :return: Complex representation of point
        :rtype: complex"""
        return complex(point[0], point[1])

    @staticmethod
    def complex_to_point(point):
        """Transform tuple to complex

        :param point: Point to convert
        :type point: complex

        :return: tuple representation of point
        :rtype: tuple"""
        return point.real, point.imag

    def rotation(self, point, center=0j, angle=0):
        """Rotate point in complex plane

        :param point: point (or list of point) to rotate
        :type point: tuple or complex
        :param center: center of rotation
        :type center: tuple or complex
        :param angle: angle of rotation
        :type angle: float

        :return: Rotated point (or list of rotated points)
        :rtype: tuple or list of tuples"""
        if type(center) != complex:
            center = self.point_to_complex(center)
        if type(point) == list:
            return [self.rotation(p, center, angle) for p in point]
        if type(point) != complex:
            point = self.point_to_complex(point)
        return self.complex_to_point(cmath.exp(complex(0, 1) * angle) * (point - center) + center)

    def homothety(self, point, center=0j, size=0):
        """Homothety of point in complex plane

        :param point: point (or list of point) to make homothety
        :type point: tuple or complex
        :param center: center of homothety
        :type center: tuple or complex
        :param size: size of homothety
        :type size: float

        :return: Homothety of point (or list of homothety of points)
        :rtype: tuple or list of tuples"""
        if type(center) != complex:
            center = self.point_to_complex(center)
        if type(point) == list:
            return [self.homothety(p, center, size) for p in point]
        if type(point) != complex:
            point = self.point_to_complex(point)
        return self.complex_to_point(size * (point - center) + center)

    def translation(self, point, vect):
        """Translate point in complex plane

        :param point: point (or list of point) to translate
        :type point: tuple or complex
        :param vect: vector of translation
        :type vect: tuple or complex

        :return: Translated point (or list of translated points)
        :rtype: tuple or list of tuples"""
        if type(vect) != complex:
            vect = self.point_to_complex(vect)
        if type(point) == list:
            return [self.translation(p, vect) for p in point]
        if type(point) != complex:
            point = self.point_to_complex(point)
        return self.complex_to_point(point + vect)

    def blanc_manger(self, origin, finish, iterations, color=None, width=0):
        """Trace blanc manger curve

        :param origin: coordinate of the starting point
        :param finish: coordinate of the ending point
        :param iterations: iterations for the drawings
        :param color: color to use for the lines
        :param width: the line width, in pixels
        :type origin: tuple
        :type finish: tuple
        :type iterations: int
        :type color: tuple
        :type width: int"""
        lenght_theoric = 2 ** iterations
        length = (((origin[0] - finish[0]) ** 2 + (origin[1] - finish[1]) ** 2) ** 0.5)

        def sawtooth(x):
            d = x - int(x)
            if d <= 1 / 2:
                return d
            return 1 - d

        def blanc_manger(x, iterations=1):
            return sum([1 / (2 ** k) * sawtooth((2 ** k) * x) for k in range(iterations)])

        points = [
            ((i / lenght_theoric) * length,
             (blanc_manger(i / lenght_theoric, iterations)) * length)
            for i in range(lenght_theoric + 1)]

        if finish[0] == origin[0]:
            angle = pi / 2
        else:
            angle = atan((finish[1] - origin[1]) / (finish[0] - origin[0]))
        points = self.rotation(points, (0, 0), angle)
        points = self.translation(points, origin)
        self.line(points, color, width)

    def von_koch_curve_flake(self, origin, radius, iterations, angle=0, color=None, width=0):
        """Draw the von koch flake on image.

        :param origin: coordinate of the center of circumscribed circle of main triangle
        :param radius: radius of circumscribed circle of main triangle
        :param iterations: iterations for the drawings
        :param angle: rotation of main triangle
        :param color: color to use for the lines
        :param width: the line width, in pixels
        :type radius: float
        :type origin: tuple
        :type iterations: int
        :type angle: float
        :type color: tuple
        :type width: int"""
        angle = angle + pi / 2
        summit_1 = (origin[0] + cos(angle) * radius, origin[1] + sin(angle) * radius)
        summit_2 = (origin[0] + cos(angle + 2 / 3 * pi) * radius, origin[1] + sin(angle + 2 / 3 * pi) * radius)
        summit_3 = (origin[0] + cos(angle - 2 / 3 * pi) * radius, origin[1] + sin(angle - 2 / 3 * pi) * radius)
        self.von_koch_curve(summit_2, summit_1, iterations, color, width)
        self.von_koch_curve(summit_3, summit_2, iterations, color, width)
        self.von_koch_curve(summit_1, summit_3, iterations, color, width)

    @staticmethod
    def _int(value):
        """Make a tuple of float coordinate into tuple of int coordinate

        :param value: Tuple to convert
        :type value: tuple

        :return: new tuple with int values
        :rtype: tuple(int, int)"""
        return int(value[0]), int(value[1])

    def von_koch_curve(self, origin, finish, iterations=1, color=None, width=0):
        """Draw the von koch curve on image.

        :param origin: coordinate of the starting point
        :param finish: coordinate of the ending point
        :param iterations: iterations for the drawings
        :param color: color to use for the lines
        :param width: the line width, in pixels
        :type origin: tuple
        :type finish: tuple
        :type iterations: int
        :type color: tuple
        :type width: int"""
        third = origin[0] + (finish[0] - origin[0]) * 1 / 3, origin[1] + (finish[1] - origin[1]) * 1 / 3
        two_third = origin[0] + (finish[0] - origin[0]) * 2 / 3, origin[1] + (finish[1] - origin[1]) * 2 / 3

        length = (((origin[0] - finish[0]) ** 2 + (origin[1] - finish[1]) ** 2) ** 0.5) / 3
        if finish[0] == origin[0]:
            angle = pi / 2
        else:
            angle = atan((finish[1] - origin[1]) / (finish[0] - origin[0]))
        angle_total = angle + pi / 3
        if origin[0] > finish[0]:
            angle_total += pi
        summit = (cos(angle_total) * length + third[0], sin(angle_total) * length + third[1])
        if iterations <= 1:
            self.line([self._int(origin), self._int(third), self._int(summit), self._int(two_third), self._int(finish)],
                      color, width)
        else:
            self.von_koch_curve(self._int(origin), self._int(third), iterations - 1, color, width)
            self.von_koch_curve(self._int(third), self._int(summit), iterations - 1, color, width)
            self.von_koch_curve(self._int(summit), self._int(two_third), iterations - 1, color, width)
            self.von_koch_curve(self._int(two_third), self._int(finish), iterations - 1, color, width)


if __name__ == "__main__":
    img = Image.new('RGB', (5000, 5000), (255, 255, 255))
    """figures = Figures(im=img)
    figures.blanc_manger((2000, 2000), (3000, 3000), 7, color=(0, 0, 0), width=2)"""
    figures = Figures(im=img)
    figures.blanc_manger((1000, 2500), (4000, 2500), 5, color=(0, 0, 0), width=3)
    img.save("D:\\Users\\louis chauvet\\Documents\\GitHub\\fractale\\test.bmp")
