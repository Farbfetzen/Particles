import random

import pygame

from src.helpers import Timer


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


class Emitter:
    def __init__(self):
        self.position = pygame.Vector2()
        self.previous_position = pygame.Vector2(self.position)
        self.particles = []
        self.time_since_last_emission = 0
        self.is_emitting = False
        self.emission_timer = Timer(1 / PARTICLES_PER_SECOND)
        self.window_bottom = pygame.display.get_window_size()[1]
        self.velocity = pygame.Vector2()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_emitting = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_emitting = False

    def update(self, dt):
        self.previous_position.update(self.position)
        self.position.update(pygame.mouse.get_pos())
        self.velocity = (self.position - self.previous_position) / dt * EMITTER_VELOCITY_FACTOR
        velocity_change = TOTAL_ACCELERATION * dt
        velocity_change_half = velocity_change / 2
        alive_particles = []
        for p in self.particles:
            if p.alive:
                alive_particles.append(p)
                p.update(dt, velocity_change, velocity_change_half)
        self.particles = alive_particles
        n_new_particles = self.emission_timer.update(dt)
        if self.is_emitting and n_new_particles > 0:
            self.emit(n_new_particles)

    def draw(self, target_surace):
        target_surace.fill(BACKGROUND_COLOR)
        if not self.is_emitting:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, self.position, 3, 1)
        for p in self.particles:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, p.position, PARTICLE_RADIUS)

    def emit(self, n_particles):
        if self.previous_position.distance_squared_to(self.position) > 0:
            for i in range(n_particles):
                position = self.position.lerp(self.previous_position, i / n_particles)
                self.particles.append(Particle(position, self.window_bottom, self.velocity))
            # TODO: Can be optimized. If distance is 10 px and n_particles is 30
            #  then I need only 10 interpolation steps with 3 particles each.
            #  Currently it interpolates 30 times which is unnecessary.
            #  Attention: In that case use distance_to instead of distance_squared_to.
        else:
            for _ in range(n_particles):
                self.particles.append(Particle(self.position, self.window_bottom, self.velocity))


class Particle:
    def __init__(self, position, y_max, emitter_velocity):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.velocity += emitter_velocity
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


