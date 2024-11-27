from dataclasses import dataclass
from math import sqrt

GRAVITATIONAL_CONSTANT = 6.6743e-11


@dataclass
class MassiveObject:
    name: str
    mass: float
    x: float
    y: float
    vx: float
    vy: float


def apply_gravity(object1: MassiveObject, object2: MassiveObject,
                  time_step: float):
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
                cos_theta: float, sin_theta: float, time_step: float):
    acceleration = force / object.mass
    x_acceleration = acceleration * cos_theta
    y_acceleration = acceleration * sin_theta

    object.vx += time_step * x_acceleration
    object.vy += time_step * y_acceleration


def main() -> None:
    sun = MassiveObject('Sun', mass=1.989e30,
                        x=0.0, y=0.0, vx=0.0, vy=0.0)
    earth = MassiveObject('Earth', mass=5.972e24,
                          x=147.61e9, y=0.0, vx=0.0, vy=-29_784.8)
    print(sun)
    print(earth)


if __name__ == '__main__':
    main()
