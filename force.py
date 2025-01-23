from dataclasses import dataclass
from itertools import combinations
from math import sqrt
from typing import Self

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

    def apply_force(self: Self, force: float,
                    cos_theta: float, sin_theta: float,
                    time_step: float) -> None:
        """
        Update the velocities for a given force at a certain angle over an
        amount of time.

        :param force: A force in Newtons
        :cos_theta, sin_theta: the cosine and sine of the force's angle
        :time_step: The time over which the force is a applied in seconds
        """
        acceleration = force / self.mass
        x_acceleration = acceleration * cos_theta
        y_acceleration = acceleration * sin_theta

        self.vx += time_step * x_acceleration
        self.vy += time_step * y_acceleration

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

    object1.apply_force(+force, cos_theta, sin_theta, time_step)
    object2.apply_force(-force, cos_theta, sin_theta, time_step)


def main() -> None:
    """
    Set up a test system using the masses, positions and velocities of the
    Sun and Earth. Simulate a year.
    """
    sun = MassiveObject('Sun', mass=1.989e30,
                        x=0.0, y=0.0, vx=0.0, vy=0.0)
    earth = MassiveObject('Earth', mass=5.972e24,
                          x=147.61e9, y=0.0, vx=0.0, vy=-29_784.8)

    days_in_one_year = 365
    seconds_in_one_day = 24 * 60 * 60
    steps = 100
    seconds_in_one_step = seconds_in_one_day / steps

    solar_system = [sun, earth]

    for day in range(days_in_one_year):
        for step in range(steps):
            for (object1, object2) in combinations(solar_system, 2):
                apply_gravity(object1, object2, seconds_in_one_step)
            for object in solar_system:
                object.update_position(seconds_in_one_step)
            print(f'{day}.{step}: (x, y) = ({earth.x:5e}, {earth.y:4e})')


if __name__ == '__main__':
    main()
