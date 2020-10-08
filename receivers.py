from point import Point


class AbstractReceiver:
    """Класс, описывающий абстрактный приёмник тока."""


class DotReceiver(AbstractReceiver):
    """Класс, описывающий точечный приёмник тока с заданными координатами на плоскости"""

    __slots__ = ["coordinate_m"]

    def __init__(self, coordinate_m: Point) -> None:
        self.coordinate_m = coordinate_m

    def __str__(self) -> str:
        return f"DotReceiver(coordinate_m={self.coordinate_m})"


class LineReceiver(AbstractReceiver):
    """Класс, описывающий приёмную линию с заданными координатами на плоскости"""

    __slots__ = ["coordinate_m", "coordinate_n"]

    def __init__(self, coordinate_m: Point, coordinate_n: Point) -> None:
        self.coordinate_m = coordinate_m
        self.coordinate_n = coordinate_n

    def __str__(self) -> str:
        return f"LineReceiver(coordinate_m={self.coordinate_m}, coordinate_n={self.coordinate_n})"
