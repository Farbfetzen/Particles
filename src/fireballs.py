import pygame

from src.base import Emitter
from src.fire import FireSimulation, FireParticle, EMISSION_DELAY


EMITTER_ACCELERATIONS = (
    pygame.Vector2(0, 750),  # gravity
)
TOTAL_EMITTER_ACCELERATION = sum(EMITTER_ACCELERATIONS, pygame.Vector2())
EMITTER_VELOCITY_FACTOR = 0.25


class FireballSimulation(FireSimulation):
    def __init__(self):
        super().__init__()
        self.emitters.clear()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.emitters.append(FireballEmitter(self.mouse_position))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.emitters:
                self.emitters[-1].release()

    def update(self, dt, mouse_position):
        self.mouse_position.update(mouse_position)
        particle_velocity_change = self.total_acceleration * dt
        particle_velocity_change_half = particle_velocity_change / 2
        alive_particles = []
        for particle in self.particles:
            particle.update(dt, particle_velocity_change, particle_velocity_change_half)
            if particle.is_alive:
                alive_particles.append(particle)
        self.particles = alive_particles
        emitter_velocity_change = TOTAL_EMITTER_ACCELERATION * dt
        emitter_velocity_change_half = emitter_velocity_change / 2
        for emitter in self.emitters:
            # TODO: remove dead emitters from list
            self.particles.extend(
                emitter.update(
                    dt,
                    self.mouse_position,
                    emitter_velocity_change,
                    emitter_velocity_change_half
                )
            )

    def clear(self):
        self.particles.clear()
        self.emitters.clear()


class FireballEmitter(Emitter):
    def __init__(self, position):
        super().__init__(position, EMISSION_DELAY, EMITTER_VELOCITY_FACTOR)
        self.is_released = False

    def update(self, dt, mouse_position, velocity_change, velocity_change_half):
        if self.is_released:
            self.velocity += velocity_change
            self.previous_position.update(self.position)
            self.position += (self.velocity - velocity_change_half) * dt
            # TODO: stop emitting particles if position is outside a certain range.
            # TODO: set self.is_alive = False if fallen below a certain range or after some time.
            n_new_particles = self.emission_timer.update(dt)
            if n_new_particles > 0:
                return self.emit(n_new_particles)
        else:
            return super().update(dt, mouse_position, True)
        return []

    def add_particle(self, position):
        return FireParticle(position)

    def release(self):
        self.is_released = True
