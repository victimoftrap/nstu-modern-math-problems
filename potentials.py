import random
from math import pi
from typing import List

from point import Point, distance


def __pre_potential__(receiver_p: Point, source_a: Point, source_b: Point) -> float:
    """Вычислить значение, используемое в вычислении потенциала.

    :param receiver_p: координата точки приёмника
    :param source_a: координата A электрода источника поля
    :param source_b: координата B электрода источника поля

    :return: значение
    """
    return 1 / distance(receiver_p, source_b) - 1 / distance(receiver_p, source_a)


def potential_difference_in_point(
        receiver_p: Point, source_a: Point, source_b: Point,
        sigma: float, amperage: float) -> float:
    """Вычислить разность потенциалов в точке P.

    :param receiver_p: точка P приёмника тока
    :param source_a: координата A электрода источника поля
    :param source_b: координата B электрода источника поля
    :param sigma: удельная электрическая проводимость
    :param amperage: сила тока

    :return: значение потенциала.
    """

    coeff = amperage / (2 * pi * sigma)
    return coeff * __pre_potential__(receiver_p, source_a, source_b)


def potential_difference_in_line(
        receiver_m: Point, receiver_n: Point, source_a: Point, source_b: Point,
        sigma: float, amperage: float) -> float:
    """Вычислить разность потенциалов в линии MN.

    :param receiver_m: точка M приёмника тока
    :param receiver_n: точка N приёмника тока
    :param source_a: координата A электрода источника поля
    :param source_b: координата B электрода источника поля
    :param sigma: удельная электрическая проводимость
    :param amperage: сила тока

    :return: значение потенциала.
    """

    coeff = amperage / (2 * pi * sigma)
    m_point_potential = __pre_potential__(receiver_m, source_a, source_b)
    n_point_potential = __pre_potential__(receiver_n, source_a, source_b)
    return coeff * (m_point_potential - n_point_potential)


def potential_derivative_in_point(
        receiver_p: Point, source_a: Point, source_b: Point,
        sigma_i: float, amperage: float) -> float:
    """Вычислить значение производной потенциала по сигма в точке sigma_i.

    :param receiver_p: точка P приёмника тока
    :param source_a: координата A электрода источника поля
    :param source_b: координата B электрода источника поля
    :param sigma_i: i-я удельная электрическая проводимость
    :param amperage: сила тока

    :return: значение производной в точке sigma_i.
    """

    sigma_square = sigma_i ** 2
    derivative_coeff = - amperage / (2 * pi * sigma_square)
    return derivative_coeff * __pre_potential__(receiver_p, source_a, source_b)


def potential_derivative_in_line(
        receiver_m: Point, receiver_n: Point, source_a: Point, source_b: Point,
        sigma_i: float, amperage: float) -> float:
    """Вычислить значение производной потенциала по сигма в линии sigma_i.

    :param receiver_m: точка M приёмника тока
    :param receiver_n: точка N приёмника тока
    :param source_a: координата A электрода источника поля
    :param source_b: координата B электрода источника поля
    :param sigma_i: i-я удельная электрическая проводимость
    :param amperage: сила тока

    :return: значение производной в точке sigma_i.
    """

    sigma_square = sigma_i ** 2
    derivative_coeff = - amperage / (2 * pi * sigma_square)

    m_point_potential = __pre_potential__(receiver_m, source_a, source_b)
    n_point_potential = __pre_potential__(receiver_n, source_a, source_b)
    return derivative_coeff * (m_point_potential - n_point_potential)


def noise(potentials: List[float], noise_number: int) -> List[float]:
    """Сделать зашумление входных данных.

    :param potentials: входные данные
    :param noise_number: количество зашумленных приемников

    :return: список с зашумлёнными данными.
    """
    noise_bound = 0.05
    receiver_number = len(potentials)
    noised_potentials = [x for x in potentials]
    for i in range(receiver_number - 1, receiver_number - noise_number - 1, -1):
        noised_potentials[i] *= (1 + random.uniform(-noise_bound, noise_bound))
    return noised_potentials
