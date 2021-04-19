# TODO: Reduce surface alpha with increasing lifetime.
#  Currently the particles just vanish suddenly.


import random

import pygame

from src import base


BACKGROUND_COLOR = pygame.Color(0, 0, 32)
PARTICLE_COLOR = pygame.Color(226, 88, 34)
PARTICLE_DIAMETER = 51
PARTICLES_PER_SECOND = 250
SECONDS_BETWEEN_EMISSIONS = 1 / PARTICLES_PER_SECOND
LIFETIME_MEAN = 0.75  # seconds
LIFETIME_SD = 0.2
SPEED_MEAN = 100  # pixels per second
SPEED_SD = 25
# Strictly speaking those are not forces but accelerations. Here it
# doesn't matter because all particles have the same mass.
FORCES = (
    pygame.Vector2(0, -400),  # updraft
)
# No need to iterate over all forces every frame if I can just use the sum.
TOTAL_FORCE = sum(FORCES, pygame.Vector2())


class Emitter(base.Emitter):
    def __init__(self):
        self.particles = []
        self.position = pygame.Vector2()
        self.time_since_last_emission = 0
        self.is_emitting = False
        self.fire_surface = pygame.Surface(pygame.display.get_window_size(), flags=pygame.SRCALPHA)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_emitting = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_emitting = False

    def update(self, dt):
        self.position.update(pygame.mouse.get_pos())
        force_dt = TOTAL_FORCE * dt
        for p in self.particles:
            p.update(dt, force_dt)
        self.particles = [p for p in self.particles if p.lifetime < p.lifetime_limit]

        if self.is_emitting:
            self.time_since_last_emission += dt
            while self.time_since_last_emission >= SECONDS_BETWEEN_EMISSIONS:
                self.time_since_last_emission -= SECONDS_BETWEEN_EMISSIONS
                self.particles.append(Particle(self.position))

    def draw(self, target_surace):
        self.fire_surface.fill((0, 0, 0, 0))
        for p in self.particles:
            self.fire_surface.blit(p.image, p.position, special_flags=pygame.BLEND_RGBA_ADD)
        target_surace.fill(BACKGROUND_COLOR)
        if not self.is_emitting:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, self.position, 3, 1)
        target_surace.blit(self.fire_surface, (0, 0))


def make_particle_image():
    image = pygame.Surface((PARTICLE_DIAMETER, PARTICLE_DIAMETER), flags=pygame.SRCALPHA)
    max_distance = (PARTICLE_DIAMETER - 1) / 2
    center = pygame.Vector2(max_distance)
    transparent_black = pygame.Color(0, 0, 0, 0)
    for x in range(PARTICLE_DIAMETER):
        for y in range(PARTICLE_DIAMETER):
            # linear interpolation (not how real light behaves)
            position = (x, y)
            distance = center.distance_to(position)
            ratio = min(distance / max_distance, 1)
            color = PARTICLE_COLOR.lerp(transparent_black, ratio)
            image.set_at(position, color)
    return image


class Particle(base.Particle):
    image = make_particle_image()

    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.position = self.position.elementwise() - PARTICLE_DIAMETER / 2
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.lifetime = 0
        self.lifetime_limit = random.gauss(LIFETIME_MEAN, LIFETIME_SD)

    def update(self, dt, force_dt):
        self.lifetime += dt
        self.velocity += force_dt
        self.position += self.velocity * dt
