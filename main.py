from point import Point
import solver

if __name__ == "__main__":
    a = Point(0, 0, 0)
    b = Point(100, 0, 0)
    sigma = 0.01
    amperage_p = 1
    receivers_p = [(Point(200, 0, 0), Point(300, 0, 0)),
                   (Point(500, 0, 0), Point(600, 0, 0)),
                   (Point(1000, 0, 0), Point(1100, 0, 0))]

    computed_sigma = solver.compute_electrical_conductivity(
        field_source=(a, b),
        receivers=receivers_p,
        true_sigma=0.1,
        start_sigma=sigma,
        amperage=amperage_p
    )
    print("Значение удельной электрической проводимости (sigma):", computed_sigma)
