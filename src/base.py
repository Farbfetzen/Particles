# import pygame
#
#
# class Simulation:
#     def __init__(self):
#         self.particles = []
#         self.emitters = []
#         self.is_emitting = False
#         self.position = pygame.Vector2()
#         self.previous_position = pygame.Vector2(self.position)
#         self.velocity = pygame.Vector2()
#
#     @property
#     def n_particles(self):
#         return len(self.particles)
#
#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             self.is_emitting = True
#         elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#             self.is_emitting = False
#
#     def update(self, dt, mouse_position):
#         self.previous_position.update(self.position)
#         self.position.update(mouse_position)
#         self.velocity = (self.position - self.previous_position) / dt * EMITTER_VELOCITY_FACTOR
#         velocity_change = TOTAL_ACCELERATION * dt
#         velocity_change_half = velocity_change / 2
#         alive_particles = []
#         for p in self.particles:
#             p.update(dt, velocity_change, velocity_change_half)
#             if p.alive:
#                 alive_particles.append(p)
#         self.particles = alive_particles
#         n_new_particles = self.emission_timer.update(dt)
#         if self.is_emitting and n_new_particles > 0:
#             self.emit(n_new_particles)
#
#     def draw(self, target_surface):
#         pass
#
#     def clear(self):
#         self.emitters.clear()
#         self.particles.clear()
#
#
# class Emitter:
#     # Handles particle emission but does not store them. Particles are stored,
#     # updated and drawn in the Simulation object.
#     def __init__(self):
#         pass
#
#     def emit(self):
#         pass
#
#
# class Particle:
#     def __init__(self):
#         pass
#
#     def update(self, dt):
#         pass
