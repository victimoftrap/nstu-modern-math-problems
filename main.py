from point import Point
import sigma_computations as sc

if __name__ == "__main__":
    field_source = (Point(0, 0, 0), Point(100, 0, 0))

    receivers = [(Point(200, 0, 0), Point(300, 0, 0)),
                 (Point(500, 0, 0), Point(600, 0, 0)),
                 (Point(1000, 0, 0), Point(1100, 0, 0))]

    true_sigma = 0.1
    initial_sigma = 0.01
    amperage = 1

    computed_sigma = sc.compute_electrical_conductivity(
        field_source=field_source,
        receivers=receivers,
        true_sigma=true_sigma,
        initial_sigma=initial_sigma,
        amperage=amperage
    )
    print("Значение удельной электрической проводимости (sigma):", computed_sigma)
