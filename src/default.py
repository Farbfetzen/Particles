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
PARTICLE_ACCELERATION = pygame.Vector2(0, 750)  # gravity
# I could also implement forces instead of accelerations but that
# is unnecessary as long as all particles have the same mass.
# Modify the emitter velocity affecting the initial particle velocity:
EMITTER_VELOCITY_FACTOR = 0.2
PARTICLE_LIMIT_RECT = pygame.Rect(-PARTICLE_DIAMETER, -PARTICLE_DIAMETER, 0, 0)


class DefaultSimulation(Simulation):
    def __init__(self):
        super().__init__(PARTICLE_ACCELERATION)
        self.emitters.append(DefaultEmitter(self.mouse_position))
        PARTICLE_LIMIT_RECT.size = pygame.display.get_window_size()
        PARTICLE_LIMIT_RECT.width += PARTICLE_DIAMETER
        PARTICLE_LIMIT_RECT.height += PARTICLE_DIAMETER


class DefaultEmitter(Emitter):
    def __init__(self, position):
        super().__init__(position, EMISSION_DELAY, EMITTER_VELOCITY_FACTOR)

    def add_particle(self, position):
        return DefaultParticle(position, self.velocity)


def make_particle_image():
    image = pygame.Surface((PARTICLE_DIAMETER, PARTICLE_DIAMETER))
    pygame.draw.circle(image, PARTICLE_COLOR, (PARTICLE_RADIUS, PARTICLE_RADIUS), PARTICLE_RADIUS)
    image.set_colorkey((0, 0, 0))
    return image


class DefaultParticle(Particle):
    image = make_particle_image()

    def __init__(self, position, emitter_velocity):
        super().__init__(position)
        self.position = self.position.elementwise() - PARTICLE_RADIUS  # center the image
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.velocity += emitter_velocity

    def update(self, dt, velocity_change, velocity_change_half):
        self.velocity += velocity_change
        self.position += (self.velocity - velocity_change_half) * dt
        if PARTICLE_LIMIT_RECT.bottom < self.position.y or \
                not PARTICLE_LIMIT_RECT.left < self.position.x < PARTICLE_LIMIT_RECT.right:
            self.is_alive = False
