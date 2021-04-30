# Improvement Ideas:
# - Fire flickers randomly. Both in brightness and direction of the flames.


import random

import pygame

from src.base import Simulation, Emitter, Particle
from src.helpers import linear_map


TRANSPARENT_BLACK = pygame.Color(0, 0, 0, 0)
FIRE_COLOR = pygame.Color(226, 88, 34)
PARTICLE_DIAMETER = 51
PARTICLES_PER_SECOND = 250
EMISSION_DELAY = 1 / PARTICLES_PER_SECOND
LIFETIME_MEAN = 1  # seconds
LIFETIME_SD = 0.1
# Time in seconds it takes for a particle to vanish. The particles start
# vanishing at lifetime - vanish_duration and die when time >= lifetime.
VANISH_DURATION = 0.5
SPEED_MEAN = 100  # pixels per second
SPEED_SD = 25
ACCELERATIONS = (
    pygame.Vector2(0, -400),  # updraft
)
TOTAL_ACCELERATION = sum(ACCELERATIONS, pygame.Vector2())


class FireSimulation(Simulation):
    def __init__(self):
        super().__init__(TOTAL_ACCELERATION, cursor_color=FIRE_COLOR)
        self.emitters.append(FireEmitter(self.mouse_position))
        self.fire_surface = pygame.Surface(
            pygame.display.get_window_size(),
            flags=pygame.SRCALPHA
        )

    def draw(self, target_surface):
        self.fire_surface.fill(TRANSPARENT_BLACK)
        for particle in self.particles:
            self.fire_surface.blit(
                particle.image,
                particle.position,
                special_flags=pygame.BLEND_RGBA_ADD
            )
        target_surface.fill(self.background_color)
        if not self.is_emitting:
            pygame.draw.circle(target_surface, self.cursor_color, self.mouse_position, 3, 1)
        target_surface.blit(self.fire_surface, (0, 0))


class FireEmitter(Emitter):
    def __init__(self, position):
        super().__init__(position, EMISSION_DELAY)

    def add_particle(self, position):
        return FireParticle(position)


def make_particle_images():
    base_image = pygame.Surface((PARTICLE_DIAMETER, PARTICLE_DIAMETER), flags=pygame.SRCALPHA)
    max_distance = (PARTICLE_DIAMETER - 1) / 2
    center = pygame.Vector2(max_distance)
    for x in range(PARTICLE_DIAMETER):
        for y in range(PARTICLE_DIAMETER):
            # linear interpolation (not how real light behaves)
            position = (x, y)
            distance = center.distance_to(position)
            ratio = min(distance / max_distance, 1)
            color = FIRE_COLOR.lerp(TRANSPARENT_BLACK, ratio)
            base_image.set_at(position, color)

    # Generate a list of images with varying transparency. Pygame doesn't let me mix
    # per pixel alpha and surface alpha so I have to blit a semitransparent layer
    # on the base image to achieve this effect.
    # The index corresponds to the transparency where 0 is transparent and 255 is opaque.
    images = []
    transparent_layer = pygame.Surface(base_image.get_size(), flags=pygame.SRCALPHA)
    for alpha in range(255, -1, -1):
        image = base_image.copy()
        transparent_layer.fill((0, 0, 0, alpha))
        image.blit(transparent_layer, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        images.append(image)

    return images


class FireParticle(Particle):
    images = make_particle_images()

    def __init__(self, position):
        super().__init__(position)
        self.position = self.position.elementwise() - PARTICLE_DIAMETER // 2  # center the image
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.image = FireParticle.images[-1]
        self.time = 0
        self.lifetime_limit = random.gauss(LIFETIME_MEAN, LIFETIME_SD)
        self.vanish_start_time = self.lifetime_limit - VANISH_DURATION
        self.is_alive = True

    def update(self, dt, velocity_change, velocity_change_half):
        self.time += dt
        if self.time >= self.vanish_start_time:
            if self.time >= self.lifetime_limit:
                self.is_alive = False
                return
            alpha = linear_map(
                self.time,
                self.vanish_start_time, self.lifetime_limit,
                255, 0
            )
            self.image = FireParticle.images[int(alpha)]
        self.velocity += velocity_change
        self.position += (self.velocity - velocity_change_half) * dt
