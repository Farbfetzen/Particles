import random

import pygame

from src.base import Simulation, Emitter, Particle
from src.helpers import linear_map


PARTICLE_COLOR = pygame.Color(64, 196, 64)
PARTICLE_DIAMETER = 10
PARTICLE_RADIUS = PARTICLE_DIAMETER / 2
PARTICLES_PER_SECOND = 100
EMISSION_DELAY = 1 / PARTICLES_PER_SECOND
SPEED_MEAN = 50  # pixels per second
SPEED_SD = 10
ACCELERATIONS = (
    pygame.Vector2(0, 750),  # gravity
)
# I could also implement forces instead of accelerations but that
# is unnecessary as long as all particles have the same mass.
TOTAL_ACCELERATION = sum(ACCELERATIONS, pygame.Vector2())
EMITTER_VELOCITY_FACTOR = 0.2
BOUNCE_MODIFIER_ALPHABETA = 3
BOUNCE_MODIFIER_MIN = 0.7
BOUNCE_MODIFIER_MAX = 0.8
MAX_BOUNCES = 10


class BounceSimulation(Simulation):
    def __init__(self):
        super().__init__(TOTAL_ACCELERATION)
        self.emitters.append(BounceEmitter(self.mouse_position))
        BounceParticle.set_limits()


class BounceEmitter(Emitter):
    def __init__(self, position):
        super().__init__(position, EMISSION_DELAY, EMITTER_VELOCITY_FACTOR)

    def add_particle(self, position):
        return BounceParticle(position, self.velocity)


def make_particle_image():
    image = pygame.Surface((PARTICLE_DIAMETER, PARTICLE_DIAMETER))
    pygame.draw.circle(image, PARTICLE_COLOR, (PARTICLE_RADIUS, PARTICLE_RADIUS), PARTICLE_RADIUS)
    image.set_colorkey((0, 0, 0))
    return image


class BounceParticle(Particle):
    image = make_particle_image()
    x_min = -PARTICLE_DIAMETER
    x_max = 1200
    y_max = 800 - PARTICLE_DIAMETER

    @classmethod
    def set_limits(cls):
        # Adjust particle position limits in case the window size
        # was changed via the command line argument:
        width, height = pygame.display.get_window_size()
        cls.x_max = width
        cls.y_max = height - PARTICLE_DIAMETER

    def __init__(self, position, emitter_velocity):
        super().__init__(position)
        self.position = self.position.elementwise() - PARTICLE_RADIUS  # center the image
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.velocity += emitter_velocity
        self.bounces = 0
        self.bounce_velocity_modifier = -linear_map(
            random.betavariate(BOUNCE_MODIFIER_ALPHABETA, BOUNCE_MODIFIER_ALPHABETA),
            out_start=BOUNCE_MODIFIER_MIN,
            out_end=BOUNCE_MODIFIER_MAX
        )

    def update(self, dt, velocity_change, velocity_change_half):
        self.velocity += velocity_change
        self.position += (self.velocity - velocity_change_half) * dt
        if self.position.y >= BounceParticle.y_max:
            self.position.y = BounceParticle.y_max * 2 - self.position.y
            self.velocity.y *= self.bounce_velocity_modifier
            self.bounces += 1
            if self.bounces >= MAX_BOUNCES:
                self.is_alive = False
        elif not BounceParticle.x_min < self.position.x < BounceParticle.x_max:
            self.is_alive = False
