from point import Point
import potentials as pots

from sys import float_info

from typing import Tuple, List


def compute_electrical_conductivity(field_source: Tuple[Point, Point], receivers: List[Tuple[Point, Point]],
                                    true_sigma: float, initial_sigma: float, amperage: float) -> float:
    """Вычислить значение удельной электрической проводимости sigma.

    :param field_source: координаты источника электрического поля
    :param receivers: координаты приёмников
    :param true_sigma: значение sigma, взятое за истинное
    :param initial_sigma: начальное значение sigma
    :param amperage: сила тока

    :return: вычисленное значение sigma.
    """
    epsilon = float_info.epsilon

    source_a = field_source[0]
    source_b = field_source[1]
    working_sigma = initial_sigma
    functional_value = float_info.max

    synthetic_potentials = []
    for receiver in receivers:
        synthetic_pot = pots.potential_difference_in_line(
            receiver_m=receiver[0],
            receiver_n=receiver[1],
            source_a=source_a,
            source_b=source_b,
            sigma=true_sigma,
            amperage=amperage
        )
        synthetic_potentials.append(synthetic_pot)

    synthetic_omega = []
    for synth_pot in synthetic_potentials:
        synthetic_omega.append(1 / synth_pot)

    while functional_value > epsilon:
        new_potentials = []
        for receiver in receivers:
            potential = pots.potential_difference_in_line(
                receiver_m=receiver[0],
                receiver_n=receiver[1],
                source_a=source_a,
                source_b=source_b,
                sigma=working_sigma,
                amperage=amperage
            )
            new_potentials.append(potential)

        functional_value = __compute_functional__(
            current_potentials=new_potentials,
            prev_potentials=synthetic_potentials,
            omega=synthetic_omega
        )

        new_sigma = __compute_new_sigma__(
            receivers=receivers,
            prev_potentials=synthetic_potentials,
            source_a=source_a,
            source_b=source_b,
            sigma_i=working_sigma,
            amperage=amperage,
            omega=synthetic_omega
        )

        print(synthetic_potentials)
        print(new_potentials)
        print("sigma =", working_sigma, "; F(sigma) =", functional_value)
        print("new sigma =", new_sigma, "\n")

        working_sigma = new_sigma

    return working_sigma


def __compute_functional__(current_potentials: List[float], prev_potentials: List[float], omega: List[float]) -> float:
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


def __compute_new_sigma__(
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
        der_potential = pots.potential_derivative_in_line(
            receivers[i][0], receivers[i][1], source_a, source_b, sigma_i, amperage
        )
        matrix_value += (omega[i] * der_potential) ** 2

        potential = pots.potential_difference_in_line(
            receivers[i][0], receivers[i][1], source_a, source_b, sigma_i, amperage
        )
        vector_value -= (omega[i] ** 2) * der_potential * (potential - prev_potentials[i])

    delta_sigma = vector_value / matrix_value
    return sigma_i + delta_sigma
