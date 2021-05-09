# Inspired by the portals in the movie Doctor Strange

# Notes:
# - Lerping may be more complicated because the emitter is rotating around the mouse.
#   So use slerp() instead? But the total movement is a combination of the mouse movement
#   and the emitter movement. But mouse movement shouldn't be much because portals don't
#   move a lot in the movies.
# - Interpolate particle color using lifetime. Start with yellow-white and end with dark red.
#   Maybe reduce necessary computation by pre-calculating a tuple of colors and then select
#   from that based on lifetime.
# - Make the ring emision more continuous without spinning the emitter faster. Maybe emit
#   the most particles from the current position but also some from further back?


import random

import pygame

from src.base import System, Emitter, Particle


PARTICLE_COLOR = pygame.Color(226, 88, 34)
PARTICLES_PER_SECOND = 500
EMISSION_DELAY = 1 / PARTICLES_PER_SECOND
PARTICLE_LIMIT_RECT = pygame.Rect(0, 0, 0, 0)
PARTICLE_LIFETIME = 0.5
PARTICLE_SPREAD_SD = 10
EMITTER_VELOCITY_FACTOR = 0.2
EMITTER_ANGULAR_SPEED = -1000  # degrees per second, negative goes counterclockwise
PORTAL_RADIUS = 200
PORTAL_GROWTH_SPEED = 100


class PortalSystem(System):
    def __init__(self):
        super().__init__(0)
        self.show_number_of_emitters = True
        PARTICLE_LIMIT_RECT.size = pygame.display.get_window_size()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.emitters.append(PortalEmitter(self.mouse_position))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.emitters.clear()

    def draw(self, target_surface):
        target_surface.fill(self.background_color)
        if not self.emitters:
            pygame.draw.circle(target_surface, self.cursor_color, self.mouse_position, 3, 1)
        for particle in self.particles:
            pygame.draw.line(
                target_surface,
                PARTICLE_COLOR,
                particle.previous_position,
                particle.position
            )


class PortalEmitter(Emitter):
    def __init__(self, position):
        super().__init__(position, EMISSION_DELAY, EMITTER_VELOCITY_FACTOR)
        self.offset = pygame.Vector2(1, 0)
        self.radius = 0

    def update(self, dt, mouse_position, is_emitting):
        if self.radius < PORTAL_RADIUS:
            self.radius = min(
                self.radius + PORTAL_GROWTH_SPEED * dt,
                PORTAL_RADIUS
            )
            self.offset.scale_to_length(self.radius)
        self.offset.rotate_ip(EMITTER_ANGULAR_SPEED * dt)
        self.previous_position.update(self.position)
        self.position.update(mouse_position + self.offset)
        self.velocity.update(
            (self.position - self.previous_position) / dt * self.emitter_velocity_factor
        )
        n_new_particles = self.emission_timer.update(dt)
        if n_new_particles > 0:
            return self.emit(n_new_particles)
        return ()

    def add_particle(self, position):
        return PortalParticle(position, self.velocity)


class PortalParticle(Particle):
    def __init__(self, position, emitter_velocity):
        super().__init__(position)
        self.previous_position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(emitter_velocity)
        self.velocity.rotate_ip(random.gauss(0, PARTICLE_SPREAD_SD))
        self.time = 0

    def update(self, dt, velocity_change, velocity_change_half):
        self.time += dt
        if self.time >= PARTICLE_LIFETIME:
            self.is_alive = False
            return
        self.previous_position.update(self.position)
        self.position += self.velocity * dt
        if not PARTICLE_LIMIT_RECT.collidepoint(self.previous_position):
            self.is_alive = False
