import random

import pygame

from src.base import Simulation, Emitter, Particle
from src.helpers import linear_map


PARTICLE_COLOR = pygame.Color(64, 196, 64)
PARTICLE_DIAMETER = 20
PARTICLE_RADIUS = PARTICLE_DIAMETER / 2
PARTICLES_PER_SECOND = 100
EMISSION_DELAY = 1 / PARTICLES_PER_SECOND
SPEED_MEAN = 200
SPEED_SD = 25
PARTICLE_ACCELERATION = 0
EMITTER_VELOCITY_FACTOR = 0.2
BOUNCE_MODIFIER_ALPHABETA = 3
BOUNCE_MODIFIER_MIN = 0.8
BOUNCE_MODIFIER_MAX = 0.9
LIFETIME_MEAN = 10
LIFETIME_SD = 2


class BounceSimulation(Simulation):
    def __init__(self):
        super().__init__(PARTICLE_ACCELERATION)
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
    x_min = 0
    y_min = 0
    x_max = 1200
    y_max = 800 - PARTICLE_DIAMETER

    @classmethod
    def set_limits(cls):
        # Adjust particle position limits in case the window size
        # was changed via the command line argument:
        width, height = pygame.display.get_window_size()
        cls.x_max = width - PARTICLE_DIAMETER
        cls.y_max = height - PARTICLE_DIAMETER

    def __init__(self, position, emitter_velocity):
        super().__init__(position)
        self.position = self.position.elementwise() - PARTICLE_RADIUS  # center the image
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.velocity += emitter_velocity
        self.bounce_velocity_modifier = -linear_map(
            random.betavariate(BOUNCE_MODIFIER_ALPHABETA, BOUNCE_MODIFIER_ALPHABETA),
            out_start=BOUNCE_MODIFIER_MIN,
            out_end=BOUNCE_MODIFIER_MAX
        )
        self.time = 0
        self.lifetime_limit = random.gauss(LIFETIME_MEAN, LIFETIME_SD)

    def update(self, dt, velocity_change, velocity_change_half):
        self.time += dt
        if self.time >= self.lifetime_limit:
            self.is_alive = False
            return
        self.position += self.velocity * dt
        if self.position.x <= BounceParticle.x_min:
            self.position.x = -self.position.x
            self.velocity.x *= self.bounce_velocity_modifier
        elif self.position.x >= BounceParticle.x_max:
            self.position.x = BounceParticle.x_max * 2 - self.position.x
            self.velocity.x *= self.bounce_velocity_modifier
        if self.position.y <= BounceParticle.y_min:
            self.position.y = -self.position.y
            self.velocity.y *= self.bounce_velocity_modifier
        elif self.position.y >= BounceParticle.y_max:
            self.position.y = BounceParticle.y_max * 2 - self.position.y
            self.velocity.y *= self.bounce_velocity_modifier
