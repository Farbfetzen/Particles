import pygame

from src.base import Emitter
from src.fire import FireSystem, FireParticle, EMISSION_DELAY


EMITTER_ACCELERATION = pygame.Vector2(0, 750)  # gravity
EMITTER_VELOCITY_FACTOR = 0.25
# Padding estimated from the size of the flames.
EMITTER_LIMIT_RECT_PADDING_X = 300
EMITTER_LIMIT_RECT_PADDING_Y = 400
EMITTER_LIMIT_RECT = pygame.Rect(
    -EMITTER_LIMIT_RECT_PADDING_X,
    -EMITTER_LIMIT_RECT_PADDING_Y,
    0,
    0
)


class FireballSystem(FireSystem):
    def __init__(self):
        super().__init__()
        self.emitters.clear()
        EMITTER_LIMIT_RECT.size = pygame.display.get_window_size()
        EMITTER_LIMIT_RECT.width += EMITTER_LIMIT_RECT_PADDING_X * 2
        EMITTER_LIMIT_RECT.height += EMITTER_LIMIT_RECT_PADDING_Y * 2
        self.show_number_of_emitters = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.emitters.append(FireballEmitter(self.mouse_position))
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.emitters:
                self.emitters[-1].release()

    def update(self, dt, mouse_position):
        self.mouse_position.update(mouse_position)

        particle_velocity_change = self.particle_acceleration * dt
        particle_velocity_change_half = particle_velocity_change / 2
        alive_particles = []
        for particle in self.particles:
            particle.update(dt, particle_velocity_change, particle_velocity_change_half)
            if particle.is_alive:
                alive_particles.append(particle)
        self.particles = alive_particles

        emitter_velocity_change = EMITTER_ACCELERATION * dt
        emitter_velocity_change_half = emitter_velocity_change / 2
        alive_emitters = []
        for emitter in self.emitters:
            self.particles.extend(
                emitter.update(
                    dt,
                    mouse_position,
                    emitter_velocity_change,
                    emitter_velocity_change_half
                )
            )
            if emitter.is_alive:
                alive_emitters.append(emitter)
        self.emitters = alive_emitters

    def clear(self):
        self.particles.clear()
        self.emitters.clear()


class FireballEmitter(Emitter):
    def __init__(self, position):
        super().__init__(position, EMISSION_DELAY, EMITTER_VELOCITY_FACTOR)
        self.is_released = False
        self.is_alive = True

    def update(self, dt, mouse_position, velocity_change, velocity_change_half):
        if self.is_released:
            self.velocity += velocity_change
            self.previous_position.update(self.position)
            self.position += (self.velocity - velocity_change_half) * dt
            if EMITTER_LIMIT_RECT.collidepoint(self.position):
                n_new_particles = self.emission_timer.update(dt)
                if n_new_particles > 0:
                    return self.emit(n_new_particles)
            elif EMITTER_LIMIT_RECT.top < self.position.y:
                self.is_alive = False
                return ()
        return super().update(dt, mouse_position, True)

    def add_particle(self, position):
        return FireParticle(position)

    def release(self):
        self.is_released = True
