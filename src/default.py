import random

import pygame

from src import base


BACKGROUND_COLOR = pygame.Color(0, 0, 32)
PARTICLE_COLOR = pygame.Color("#e25822")
PARTICLE_RADIUS = 5
PARTICLES_PER_SECOND = 100
SECONDS_BETWEEN_EMISSIONS = 1 / PARTICLES_PER_SECOND
MOUSE_IS_VISIBLE = False
MAX_LIFETIME = 1  # in seconds
SPEED = 100  # pixels per second


class Emitter(base.Emitter):
    def __init__(self):
        self.particles = []
        self.position = pygame.Vector2()
        self.time_since_last_emission = 0
        self.is_emitting = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_emitting = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_emitting = False

    def update(self, dt):
        self.position.update(pygame.mouse.get_pos())
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.lifetime < MAX_LIFETIME]

        if self.is_emitting:
            self.time_since_last_emission += dt
            while self.time_since_last_emission >= SECONDS_BETWEEN_EMISSIONS:
                self.time_since_last_emission -= SECONDS_BETWEEN_EMISSIONS
                self.particles.append(Particle(self.position))

    def draw(self, target_surace):
        target_surace.fill(BACKGROUND_COLOR)
        pygame.draw.circle(target_surace, PARTICLE_COLOR, self.position, 3, 1)
        for p in self.particles:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, p.position, PARTICLE_RADIUS, 0)


class Particle(base.Particle):
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(SPEED, 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.lifetime = 0

    def update(self, dt):
        self.lifetime += dt
        self.position += self.velocity * dt
