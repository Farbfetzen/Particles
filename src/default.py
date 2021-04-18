import random

import pygame

WINDOW_SIZE = (800, 600)
FPS = 60
BACKGROUND_COLOR = pygame.Color(0, 0, 32)
PARTICLE_COLOR = pygame.Color(230, 230, 230)
PARTICLE_RADIUS = 5
PARTICLES_PER_SECOND = 100
SECONDS_BETWEEN_EMISSIONS = 1 / PARTICLES_PER_SECOND
MOUSE_IS_VISIBLE = False
MAX_LIFETIME = 1  # in seconds
VELOCITY = 100  # pixels per second


class Emitter:
    def __init__(self):
        self.particles = []
        self.position = pygame.Vector2()
        self.time_since_last_emission = 0

    def handle_event(self, event):
        pass

    def update(self, dt):
        self.position.update(pygame.mouse.get_pos())
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.lifetime < MAX_LIFETIME]

        self.time_since_last_emission += dt
        while self.time_since_last_emission >= SECONDS_BETWEEN_EMISSIONS:
            self.emit()
            self.time_since_last_emission -= SECONDS_BETWEEN_EMISSIONS

    def emit(self):
        velocity = pygame.Vector2(VELOCITY, 0)
        velocity.rotate_ip(random.uniform(0, 360))
        self.particles.append(Particle(self.position, velocity))

    def draw(self, target_surace):
        target_surace.fill(BACKGROUND_COLOR)
        # pygame.draw.circle(target_surace, (255, 100, 100), self.position, 2)  # DEBUG
        for p in self.particles:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, p.position, PARTICLE_RADIUS, 0)


class Particle:
    def __init__(self, position, velocity):
        self.position = pygame.Vector2(position)
        self.velocity = velocity
        self.lifetime = 0

    def update(self, dt):
        self.lifetime += dt
        self.position += self.velocity * dt
