import random

import pygame

from src import base


BACKGROUND_COLOR = pygame.Color(0, 0, 32)
PARTICLE_COLOR = pygame.Color("#e25822")
PARTICLE_RADIUS = 5
PARTICLES_PER_SECOND = 500
SECONDS_BETWEEN_EMISSIONS = 1 / PARTICLES_PER_SECOND
MOUSE_IS_VISIBLE = False
LIFETIME_MEAN = 1  # seconds
LIFETIME_SD = 0.25
SPEED_MEAN = 100  # pixels per second
SPEED_SD = 25
# Strictly speaking those are not forces but accelerations. Here it
# doesn't matter because all particles have the same mass.
FORCES = (
    pygame.Vector2(0, 500),  # gravity
    pygame.Vector2(300, 0),  # wind
)
# No need to iterate over all forces every frame if I can just use the sum.
TOTAL_FORCE = sum(FORCES, pygame.Vector2())


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
        target_surace.fill(BACKGROUND_COLOR)
        pygame.draw.circle(target_surace, PARTICLE_COLOR, self.position, 3, 1)
        for p in self.particles:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, p.position, PARTICLE_RADIUS, 0)


class Particle(base.Particle):
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.lifetime = 0
        self.lifetime_limit = random.gauss(LIFETIME_MEAN, LIFETIME_SD)

    def update(self, dt, force_dt):
        self.lifetime += dt
        self.velocity += force_dt
        self.position += self.velocity * dt
