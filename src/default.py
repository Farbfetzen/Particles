import random

import pygame

from src.base import Simulation, Emitter, Particle


PARTICLE_COLOR = pygame.Color(220, 220, 220)
PARTICLE_DIAMETER = 10
PARTICLE_RADIUS = PARTICLE_DIAMETER / 2
PARTICLES_PER_SECOND = 500
EMISSION_DELAY = 1 / PARTICLES_PER_SECOND
SPEED_MEAN = 150  # pixels per second
SPEED_SD = 20
ACCELERATIONS = (
    pygame.Vector2(0, 750),  # gravity
)
# I could also implement forces instead of accelerations but that
# is unnecessary as long as all particles have the same mass.
TOTAL_ACCELERATION = sum(ACCELERATIONS, pygame.Vector2())
# Modify the emitter velocity affecting the initial particle velocity:
EMITTER_VELOCITY_FACTOR = 0.2


class DefaultSimulation(Simulation):
    def __init__(self):
        super().__init__(TOTAL_ACCELERATION)
        self.emitters.append(DefaultEmitter(self.mouse_position))


class DefaultEmitter(Emitter):
    def __init__(self, position):
        super().__init__(position, EMISSION_DELAY, EMITTER_VELOCITY_FACTOR)
        self.window_right, self.window_bottom = pygame.display.get_window_size()

    def add_particle(self, position):
        return DefaultParticle(position, self.window_right, self.window_bottom, self.velocity)


def make_particle_image():
    image = pygame.Surface((PARTICLE_DIAMETER, PARTICLE_DIAMETER))
    pygame.draw.circle(image, PARTICLE_COLOR, (PARTICLE_RADIUS, PARTICLE_RADIUS), PARTICLE_RADIUS)
    image.set_colorkey((0, 0, 0))
    return image


class DefaultParticle(Particle):
    image = make_particle_image()

    def __init__(self, position, x_max, y_max, emitter_velocity):
        super().__init__(position)
        self.position = self.position.elementwise() - PARTICLE_RADIUS  # center the image
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.velocity += emitter_velocity
        self.x_min = -PARTICLE_DIAMETER
        self.x_max = x_max
        self.y_max = y_max

    def update(self, dt, velocity_change, velocity_change_half):
        if self.position.y >= self.y_max or not self.x_min < self.position.x < self.x_max:
            self.is_alive = False
        else:
            self.velocity += velocity_change
            # Accurate mouse_position under gravity.:
            self.position += (self.velocity - velocity_change_half) * dt
            # This one is inaccurate but also ok. The difference gets smaller
            # with time and becomes less than 1 % after about 120 steps.
            # self.mouse_position += self.velocity * dt
