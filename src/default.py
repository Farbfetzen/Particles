import random
from math import ceil

import pygame


BACKGROUND_COLOR = pygame.Color(0, 0, 32)
PARTICLE_COLOR = pygame.Color(220, 220, 220)
PARTICLE_RADIUS = 5
PARTICLES_PER_SECOND = 2
SPEED_MEAN = 150  # pixels per second
SPEED_SD = 50
ACCELERATIONS = (
    pygame.Vector2(0, 750),  # gravity
)
# I could also implement forces instead of accelerations but that
# is unnecessary as long as all particles have the same mass.
TOTAL_ACCELERATION = sum(ACCELERATIONS, pygame.Vector2())
EMISSION_EVENT_ID = pygame.event.custom_type()
MAX_EMISSION_DISTANCE = 10


class Emitter:
    def __init__(self):
        self.particles = []
        self.position = pygame.Vector2()
        self.previous_position = pygame.Vector2(self.position)
        self.time_since_last_emission = 0
        self.is_emitting = False
        self.window_bottom = pygame.display.get_window_size()[1]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_emitting = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_emitting = False

    def update(self, dt):
        self.previous_position.update(self.position)
        self.position.update(pygame.mouse.get_pos())
        self.particles = [p for p in self.particles if p.alive]
        velocity_change = TOTAL_ACCELERATION * dt
        velocity_change_half = velocity_change / 2
        alive_particles = []
        for p in self.particles:
            if p.alive:
                alive_particles.append(p)
                p.update(dt, velocity_change, velocity_change_half)
        self.particles = alive_particles
        if self.is_emitting:
            self.emit(round(PARTICLES_PER_SECOND * dt))

    def draw(self, target_surace):
        target_surace.fill(BACKGROUND_COLOR)
        if not self.is_emitting:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, self.position, 3, 1)
        for p in self.particles:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, p.position, PARTICLE_RADIUS)

    def emit(self, n_particles):
        d = self.previous_position.distance_to(self.position)
        if d > MAX_EMISSION_DISTANCE:
            divisions = ceil(d / MAX_EMISSION_DISTANCE)
            n_particles_per_step = n_particles // divisions
            debug = 0
            for i in range(1, divisions):
                debug += 1
                r = i / divisions
                position = self.previous_position.lerp(self.position, r)
                for _ in range(n_particles_per_step):
                    self.particles.append(Particle(position, self.window_bottom))
                n_particles -= n_particles_per_step
            for _ in range(n_particles):
                self.particles.append(Particle(self.position, self.window_bottom))
        else:
            for _ in range(n_particles):
                self.particles.append(Particle(self.position, self.window_bottom))


class Particle:
    def __init__(self, position, y_max):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.y_max = y_max + PARTICLE_RADIUS
        self.alive = True

    def update(self, dt, velocity_change, velocity_change_half):
        if self.position.y >= self.y_max:
            self.alive = False
        else:
            self.velocity += velocity_change
            # Accurate position under gravity.:
            self.position += (self.velocity - velocity_change_half) * dt
            # This one is inaccurate but also ok. The difference gets smaller
            # with time and becomes less than 1 % after about 120 steps.
            # self.position += self.velocity * dt


