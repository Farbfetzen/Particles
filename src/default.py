import random

import pygame

from src import base


BACKGROUND_COLOR = pygame.Color(0, 0, 32)
PARTICLE_COLOR = pygame.Color(220, 220, 220)
PARTICLE_RADIUS = 5
PARTICLES_PER_SECOND = 500
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


class Simulation(base.Simulation):
    def __init__(self):
        super().__init__(BACKGROUND_COLOR, PARTICLE_COLOR, PARTICLE_RADIUS, TOTAL_ACCELERATION)
        self.emitters.append(Emitter(pygame.display.get_window_size()))


class Emitter(base.Emitter):
    def __init__(self, window_size):
        super().__init__(1 / PARTICLES_PER_SECOND, EMITTER_VELOCITY_FACTOR)
        self.window_right, self.window_bottom = window_size

    def add_particle(self, position, particle_list):
        particle_list.append(
            Particle(position, self.window_right, self.window_bottom, self.velocity)
        )


class Particle:
    def __init__(self, position, x_max, y_max, emitter_velocity):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.velocity += emitter_velocity
        self.x_min = -PARTICLE_RADIUS
        self.x_max = x_max + PARTICLE_RADIUS
        self.y_max = y_max + PARTICLE_RADIUS
        self.is_alive = True

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
