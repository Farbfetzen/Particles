import pygame

import src.fire


BACKGROUND_COLOR = pygame.Color(0, 0, 32)
CURSOR_COLOR = pygame.Color(220, 220, 220)
ACCELERATIONS = (
    pygame.Vector2(0, 750),  # gravity
)
TOTAL_ACCELERATION = sum(ACCELERATIONS, pygame.Vector2())
EMITTER_VELOCITY_FACTOR = 0.25


class Emitter:
    def __init__(self):
        self.position = pygame.Vector2()
        self.previous_position = pygame.Vector2(self.position)
        self.particles = []
        self.is_emitting = False
        self.velocity = pygame.Vector2()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_emitting = True
            self.emit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_emitting = False
            self.particles[-1].release(self.velocity)

    def update(self, dt, mouse_position):
        self.previous_position.update(self.position)
        self.position.update(mouse_position)
        self.velocity = (self.position - self.previous_position) / dt * EMITTER_VELOCITY_FACTOR
        velocity_change = TOTAL_ACCELERATION * dt
        velocity_change_half = velocity_change / 2
        alive_particles = []
        for p in self.particles:
            if p.alive:
                alive_particles.append(p)
                p.update(dt, self.position, velocity_change, velocity_change_half)
        self.particles = alive_particles

    def draw(self, target_surface):
        target_surface.fill(BACKGROUND_COLOR)
        if not self.is_emitting:
            pygame.draw.circle(target_surface, CURSOR_COLOR, self.position, 3, 1)
        for p in self.particles:
            p.draw(target_surface)

    def emit(self):
        self.particles.append(Particle(self.position))

    def clear(self):
        self.particles.clear()


class Particle:
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2()
        self.alive = True
        self.emitter = src.fire.Emitter()
        self.emitter.position.update(self.position)
        self.emitter.previous_position.update(self.position)
        self.emitter.is_emitting = True
        self.is_released = False

    def release(self, emitter_velocity):
        self.is_released = True
        self.velocity.update(emitter_velocity)

    def update(self, dt, position, velocity_change, velocity_change_half):
        if self.is_released:
            self.released_update(dt, velocity_change, velocity_change_half)
        else:
            self.held_update(dt, position)

    def held_update(self, dt, position):
        # Particle is held at mouse position.
        self.position.update(position)
        self.emitter.update(dt, position)

    def released_update(self, dt, velocity_change, velocity_change_half):
        # Particle has been released from the mouse.
        if not self.emitter.particles:
            self.alive = False
            return
        self.velocity += velocity_change
        self.position += (self.velocity - velocity_change_half) * dt
        self.emitter.update(dt, self.position)

    def draw(self, target_surface):
        self.emitter.draw(target_surface, False)
