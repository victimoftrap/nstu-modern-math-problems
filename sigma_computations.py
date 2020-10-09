from point import Point
from receivers import AbstractReceiver, DotReceiver, LineReceiver
import potentials as pots

from sys import float_info

from typing import Tuple, List


def compute_electrical_conductivity(field_source: Tuple[Point, Point], receivers: List[AbstractReceiver],
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
    prev_functional_value = float_info.min

    synthetic_potentials = []
    for receiver in receivers:
        synthetic_pot = 0
        if isinstance(receiver, LineReceiver):
            synthetic_pot = pots.potential_difference_in_line(
                receiver_m=receiver.coordinate_m,
                receiver_n=receiver.coordinate_n,
                source_a=source_a,
                source_b=source_b,
                sigma=true_sigma,
                amperage=amperage
            )

        if isinstance(receiver, DotReceiver):
            synthetic_pot = pots.potential_difference_in_point(
                receiver_p=receiver.coordinate_m,
                source_a=source_a,
                source_b=source_b,
                sigma=true_sigma,
                amperage=amperage
            )

        synthetic_potentials.append(synthetic_pot)

    synthetic_omega = []
    for synth_pot in synthetic_potentials:
        synthetic_omega.append(1 / synth_pot)

    while abs(functional_value - prev_functional_value) > epsilon:
        new_potentials = []
        for receiver in receivers:
            potential = 0
            if isinstance(receiver, LineReceiver):
                potential = pots.potential_difference_in_line(
                    receiver_m=receiver.coordinate_m,
                    receiver_n=receiver.coordinate_n,
                    source_a=source_a,
                    source_b=source_b,
                    sigma=working_sigma,
                    amperage=amperage
                )

            if isinstance(receiver, DotReceiver):
                potential = pots.potential_difference_in_point(
                    receiver_p=receiver.coordinate_m,
                    source_a=source_a,
                    source_b=source_b,
                    sigma=working_sigma,
                    amperage=amperage
                )
            new_potentials.append(potential)

        prev_functional_value = functional_value
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

        print("synth pots:", synthetic_potentials)
        print("pots:", new_potentials)
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
        receivers: List[AbstractReceiver], prev_potentials: List[float],
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
        receiver = receivers[i]
        potential = 0
        pot_derivative = 0

        if isinstance(receiver, LineReceiver):
            pot_derivative = pots.potential_derivative_in_line(
                receiver.coordinate_m, receiver.coordinate_n, source_a, source_b, sigma_i, amperage
            )
            potential = pots.potential_difference_in_line(
                receiver.coordinate_m, receiver.coordinate_n, source_a, source_b, sigma_i, amperage
            )

        if isinstance(receiver, DotReceiver):
            pot_derivative = pots.potential_derivative_in_point(
                receiver.coordinate_m, source_a, source_b, sigma_i, amperage
            )
            potential = pots.potential_derivative_in_point(
                receiver.coordinate_m, source_a, source_b, sigma_i, amperage
            )

        vector_value -= (omega[i] ** 2) * pot_derivative * (potential - prev_potentials[i])
        matrix_value += (omega[i] * pot_derivative) ** 2

    delta_sigma = vector_value / matrix_value
    return sigma_i + delta_sigma
