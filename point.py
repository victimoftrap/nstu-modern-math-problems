from collections import namedtuple
from math import sqrt

Point = namedtuple("Point", ["x", "y", "z"])
Point.__doc__ = """Именованный кортеж, описывающий точку в трёхмерной области. Point[X, Y, Z]"""


def distance(point1: Point, point2: Point) -> float:
    """Рассчитать расстояние между двумя точками.

    :param point1: первая точка
    :param point2: вторая точка

    :return: расстояние между точками.
    """

    x = (point2.x - point1.x) ** 2
    y = (point2.y - point1.y) ** 2
    z = (point2.z - point1.z) ** 2
    return sqrt(x + y + z)
