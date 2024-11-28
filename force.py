from dataclasses import dataclass
from itertools import combinations
from math import sqrt
from typing_extensions import Self

GRAVITATIONAL_CONSTANT = 6.6743e-11


@dataclass
class MassiveObject:
    """
    A simple class representing a massive object, with position and velocity.

    :param mass: Mass in kilograms
    :param x, y: Position in meters
    :param vx, vy: Velocity in meters per second
    """
    name: str
    mass: float
    x: float
    y: float
    vx: float
    vy: float

    def update_position(self: Self, time_step: float) -> None:
        """
        Update the position of the MassiveObject using its velocity
        and time_step.

        :param time_step: The time step in seconds
        """
        self.x += self.vx * time_step
        self.y += self.vy * time_step


def apply_gravity(object1: MassiveObject, object2: MassiveObject,
                  time_step: float) -> None:
    """
    Step two MassiveObjects using their mutual gravity over time_step

    :param object1, object2: Two MassiveObjects
    :param time_step: the time over which the interaction happens in seconds
    """
    x_distance = object2.x - object1.x
    y_distance = object2.y - object1.y

    distance_squared = x_distance * x_distance + y_distance * y_distance
    distance = sqrt(distance_squared)

    cos_theta = x_distance / distance
    sin_theta = y_distance / distance

    force = GRAVITATIONAL_CONSTANT * object1.mass * object2.mass \
        / distance_squared

    apply_force(object1, +force, cos_theta, sin_theta, time_step)
    apply_force(object2, -force, cos_theta, sin_theta, time_step)


def apply_force(object: MassiveObject, force: float,
                cos_theta: float, sin_theta: float, time_step: float) -> None:
    """
    Update the velocities of two MassiveObjects for a given force at a certain
    angle over an amount of time.

    :param object1, object2: The two MassiveObjects mutually affecting each
    other
    :param force: A force in Newtons
    :cos_theta, sin_theta: the cosine and sine of the force's angle
    :time_step: The time over which the force is a applied in seconds
    """
    acceleration = force / object.mass
    x_acceleration = acceleration * cos_theta
    y_acceleration = acceleration * sin_theta

    object.vx += time_step * x_acceleration
    object.vy += time_step * y_acceleration


def main() -> None:
    """
    Set up a test system using the masses, positions and velocities of the
    Sun and Earth. Simulate a year.
    """
    sun = MassiveObject('Sun', mass=1.989e30,
                        x=0.0, y=0.0, vx=0.0, vy=0.0)
    earth = MassiveObject('Earth', mass=5.972e24,
                          x=147.61e9, y=0.0, vx=0.0, vy=-29_784.8)

    one_year = 365
    one_day = 24 * 60 * 60
    steps = 100

    solar_system = [sun, earth]

    for day in range(one_year):
        for step in range(steps):
            for (object1, object2) in combinations(solar_system, 2):
                apply_gravity(object1, object2, one_day/steps)
            for object in solar_system:
                object.update_position(one_day/steps)
            print(f'{day}.{step}: (x, y) = ({earth.x:5e}, {earth.y:4e})')


if __name__ == '__main__':
    main()
