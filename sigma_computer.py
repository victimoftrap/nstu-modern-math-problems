import potentials as pots
from point import Point

from typing import List, Tuple


def compute_functional(current_potentials: List[float], prev_potentials: List[float], omega: List[float]) -> float:
    """Получить значение функционала.

    :param current_potentials: текущеие значения потениалов
    :param prev_potentials: синтетические значения потенциалов
    :param omega: весовые коэффициенты

    :return: значение функционала.
    """

    size = len(omega)
    result = 0
    for i in range(size):
        result += (omega[i] * (current_potentials[i] - prev_potentials[i])) ** 2
    return result


def compute_new_sigma(
        receivers: List[Tuple[Point, Point]], prev_potentials: List[float],
        source_a: Point, source_b: Point,
        sigma_i: float, amperage: float, omega: List[float]) -> float:
    """Вычислить новое значение sigma.

    Tuple[List[List[float]], List[float]] - СЛАУ.
        Первая компонента: List[List[float]] - матрица СЛАУ размером 1.
        Вторая компонента: List[float] - правая часть СЛАУ, вектор размерности 1.

    :param receivers: координаты точек приёмников
    :param prev_potentials: список потенциалов, вычисленных с предыдущей sigma
    :param source_a: координата A электрода источника поля
    :param source_b: координата B электрода источника поля
    :param sigma_i: i-я удельная электрическая проводимость
    :param amperage: сила тока
    :param omega: весовые коэффициенты

    :return: новая sigma
    """

    receiver_quantity = len(receivers)
    matrix_value = 0
    vector_value = 0

    for i in range(receiver_quantity):
        der_potential = pots.compute_potential_derivative(
            receivers[i][0], receivers[i][1], source_a, source_b, sigma_i, amperage
        )
        matrix_value += (omega[i] * der_potential) ** 2

        potential = pots.compute_electric_field_potential_difference(
            receivers[i][0], receivers[i][1], source_a, source_b, sigma_i, amperage
        )
        vector_value -= (omega[i] ** 2) * der_potential * (potential - prev_potentials[i])

    delta_sigma = vector_value / matrix_value
    return sigma_i + delta_sigma
