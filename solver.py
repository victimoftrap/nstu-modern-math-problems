from point import Point
import potentials as pots
import sigma_computer as sc

from sys import float_info

from typing import Tuple, List


def compute_electrical_conductivity(field_source: Tuple[Point, Point], receivers: List[Tuple[Point, Point]],
                                    true_sigma: float, start_sigma: float, amperage: float) -> float:
    """Вычислить значение удельной электрической проводимости sigma.

    :param field_source: координаты источника электрического поля
    :param receivers: координаты приёмников
    :param true_sigma: значение sigma, взятое за истинное
    :param start_sigma: начальное значение sigma
    :param amperage: сила тока

    :return: вычисленное значение sigma.
    """
    epsilon = float_info.epsilon

    source_a = field_source[0]
    source_b = field_source[1]
    working_sigma = start_sigma
    functional_value = float_info.max

    synthetic_potentials = []
    for receiver in receivers:
        synthetic_pot = pots.compute_electric_field_potential_difference(
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
            potential = pots.compute_electric_field_potential_difference(
                receiver_m=receiver[0],
                receiver_n=receiver[1],
                source_a=source_a,
                source_b=source_b,
                sigma=working_sigma,
                amperage=amperage
            )
            new_potentials.append(potential)

        functional_value = sc.compute_functional(
            current_potentials=new_potentials,
            prev_potentials=synthetic_potentials,
            omega=synthetic_omega
        )

        new_sigma = sc.compute_new_sigma(
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
