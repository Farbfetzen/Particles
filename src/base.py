from abc import ABC, abstractmethod

import pygame

from src.helpers import Timer


class Simulation:
    def __init__(self, background_color, particle_color, particle_radius, total_acceleration):
        self.particles = []
        self.emitters = []
        self.is_emitting = False
        self.mouse_position = pygame.Vector2()
        self.previous_mouse_position = pygame.Vector2(self.mouse_position)
        self.background_color = background_color
        self.particle_color = particle_color
        self.particle_radius = particle_radius
        self.total_acceleration = total_acceleration

    @property
    def n_particles(self):
        return len(self.particles)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_emitting = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_emitting = False

    def update(self, dt, mouse_position):
        self.previous_mouse_position.update(self.mouse_position)
        self.mouse_position.update(mouse_position)
        velocity_change = self.total_acceleration * dt
        velocity_change_half = velocity_change / 2
        alive_particles = []
        for particle in self.particles:
            particle.update(dt, velocity_change, velocity_change_half)
            if particle.is_alive:
                alive_particles.append(particle)
        self.particles = alive_particles
        for emitter in self.emitters:
            self.particles.extend(
                emitter.update(dt, self.mouse_position, self.is_emitting)
            )

    def draw(self, target_surface):
        target_surface.fill(self.background_color)
        if not self.is_emitting:
            pygame.draw.circle(target_surface, self.particle_color, self.mouse_position, 3, 1)
        for particle in self.particles:
            pygame.draw.circle(target_surface, self.particle_color,
                               particle.position, self.particle_radius)

    def clear(self):
        self.particles.clear()


class Emitter(ABC):
    def __init__(self, emission_timer_delay, emitter_velocity_factor=0):
        self.position = pygame.Vector2()
        self.previous_position = pygame.Vector2()
        self.emission_timer = Timer(emission_timer_delay)
        self.emitter_velocity_factor = emitter_velocity_factor
        self.velocity = pygame.Vector2() if emitter_velocity_factor != 0 else None

    def update(self, dt, mouse_position, is_emitting):
        self.previous_position.update(self.position)
        self.position.update(mouse_position)
        if self.velocity is not None:
            self.velocity.update(
                (self.position - self.previous_position) / dt * self.emitter_velocity_factor
            )
        n_new_particles = self.emission_timer.update(dt)
        if is_emitting and n_new_particles > 0:
            return self.emit(n_new_particles)
        return []

    def emit(self, n_particles):
        if self.previous_position.distance_squared_to(self.position) > 0:
            new_particles = []
            for i in range(n_particles):
                position = self.position.lerp(self.previous_position, i / n_particles)
                new_particles.append(self.add_particle(position))
        else:
            new_particles = [self.add_particle(self.position) for _ in range(n_particles)]
        return new_particles

    @abstractmethod
    def add_particle(self, position):
        # Instantiate a particle at position and return it.
        pass


class Particle(ABC):
    def __init__(self, position):
        self.position = pygame.Vector2(position)

    @abstractmethod
    def update(self, dt, velocity_change, velocity_change_half):
        pass
