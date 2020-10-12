from point import Point
from receivers import LineReceiver, DotReceiver
from potentials import noise
import sigma_computations as sc

if __name__ == "__main__":
    field_source = (Point(0, 0, 0), Point(100, 0, 0))

    # receivers = [LineReceiver(Point(200, 0, 0), Point(300, 0, 0)),
    #             LineReceiver(Point(500, 0, 0), Point(600, 0, 0)),
    #             LineReceiver(Point(1000, 0, 0), Point(1100, 0, 0))]

    receivers = [DotReceiver(Point(200, 0, 0)),
                 DotReceiver(Point(500, 0, 0)),
                 DotReceiver(Point(1000, 0, 0))]

    true_sigma = 0.1
    initial_sigma = 0.01
    amperage = 1

    potentials = sc.generate_synthetic_potentials(
        field_source=field_source,
        receivers=receivers,
        true_sigma=true_sigma,
        amperage=amperage
    )

    computed_sigma = sc.compute_electrical_conductivity(
        field_source=field_source,
        receivers=receivers,
        synthetic_potentials=potentials,
        initial_sigma=initial_sigma,
        amperage=amperage
    )

    print("Значение удельной электрической проводимости (sigma):", computed_sigma)

    noised_potentials = noise(potentials)

    print("Зашумленные данные:", noised_potentials)

    computed_sigma_noised = sc.compute_electrical_conductivity(
        field_source=field_source,
        receivers=receivers,
        synthetic_potentials=noised_potentials,
        initial_sigma=initial_sigma,
        amperage=amperage
    )

    print("Значение удельной электрической проводимости (sigma) на зашумленных данных:", computed_sigma_noised)
