# Improvement Ideas:
# - Fire flickers randomly. Both in brightness and direction of the flames.


import random

import pygame

from src.helpers import linear_map, Timer


BACKGROUND_COLOR = pygame.Color(0, 0, 32)
TRANSPARENT_BLACK = pygame.Color(0, 0, 0, 0)
PARTICLE_COLOR = pygame.Color(226, 88, 34)
PARTICLE_DIAMETER = 51
PARTICLES_PER_SECOND = 250
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


class Emitter:
    def __init__(self):
        self.position = pygame.Vector2()
        self.previous_position = pygame.Vector2(self.position)
        self.particles = []
        self.is_emitting = False
        self.emission_timer = Timer(1 / PARTICLES_PER_SECOND)
        self.fire_surface = pygame.Surface(pygame.display.get_window_size(), flags=pygame.SRCALPHA)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_emitting = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_emitting = False

    def update(self, dt):
        self.previous_position.update(self.position)
        self.position.update(pygame.mouse.get_pos())
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
        self.fire_surface.fill(TRANSPARENT_BLACK)
        for p in self.particles:
            self.fire_surface.blit(p.image, p.position, special_flags=pygame.BLEND_RGBA_ADD)
        target_surace.fill(BACKGROUND_COLOR)
        if not self.is_emitting:
            pygame.draw.circle(target_surace, PARTICLE_COLOR, self.position, 3, 1)
        target_surace.blit(self.fire_surface, (0, 0))

    def emit(self, n_particles):
        if self.previous_position.distance_squared_to(self.position) > 0:
            for i in range(n_particles):
                position = self.position.lerp(self.previous_position, i / n_particles)
                self.particles.append(Particle(position))
        else:
            for _ in range(n_particles):
                self.particles.append(Particle(self.position))

    def clear(self):
        self.particles.clear()


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
            color = PARTICLE_COLOR.lerp(TRANSPARENT_BLACK, ratio)
            base_image.set_at(position, color)

    # Generate a list of images with varying transparency. Pygame doesn't let me mix
    # per pixel alpha and surface alpha so I have to blit a semitransparent layer
    # on the base image to achieve this effect.
    # The index corresponsds to the transparency where 0 is transparent and 255 is opaque.
    images = []
    transparent_layer = pygame.Surface(base_image.get_size(), flags=pygame.SRCALPHA)
    for alpha in range(255, -1, -1):
        image = base_image.copy()
        transparent_layer.fill((0, 0, 0, alpha))
        image.blit(transparent_layer, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        images.append(image)

    return images


class Particle:
    images = make_particle_images()

    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.position = self.position.elementwise() - PARTICLE_DIAMETER // 2  # center the image
        self.velocity = pygame.Vector2(random.gauss(SPEED_MEAN, SPEED_SD), 0)
        self.velocity.rotate_ip(random.uniform(0, 360))
        self.image = Particle.images[-1]
        self.time = 0
        self.lifetime_limit = random.gauss(LIFETIME_MEAN, LIFETIME_SD)
        self.vanish_start_time = self.lifetime_limit - VANISH_DURATION
        self.alive = True

    def update(self, dt, velocity_change, velocity_change_half):
        self.time += dt
        if self.time >= self.vanish_start_time:
            if self.time >= self.lifetime_limit:
                self.alive = False
                return
            alpha = linear_map(
                self.time,
                self.vanish_start_time, self.lifetime_limit,
                255, 0
            )
            self.image = Particle.images[int(alpha)]
        self.velocity += velocity_change
        self.position += (self.velocity - velocity_change_half) * dt
