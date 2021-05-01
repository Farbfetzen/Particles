import pygame
import pygame.freetype

from src.bounce import BounceSimulation
from src.default import DefaultSimulation
from src.fire import FireSimulation
from src.fireballs import FireballSimulation


SIMS = {
    "bounce": BounceSimulation,
    "default": DefaultSimulation,
    "fire": FireSimulation,
    "fireballs": FireballSimulation
}
SIM_NAMES = sorted(list(SIMS.keys()))


def run(sim_name, window_size):
    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Particles")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    paused = False

    sim = SIMS[sim_name]()
    sim_index = SIM_NAMES.index(sim_name)

    show_info = True
    font = pygame.freetype.SysFont(("consolas", "inconsolata", "monospace"), 16)
    font.fgcolor = pygame.Color((220, 220, 220))
    line_spacing = pygame.Vector2(0, font.get_sized_height())
    text_margin = pygame.Vector2(5, 5)

    while True:
        dt = clock.tick(60) / 1000  # in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_F1:
                    show_info = not show_info
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    pygame.mouse.set_visible(paused)
                elif event.key == pygame.K_DELETE:
                    sim.clear()
                elif event.key == pygame.K_n:
                    # Switch to the next simulation
                    sim_index = (sim_index + 1) % len(SIM_NAMES)
                    sim_name = SIM_NAMES[sim_index]
                    sim = SIMS[sim_name]()
            sim.handle_event(event)

        if not paused:
            sim.update(dt, pygame.mouse.get_pos())

        sim.draw(window)

        if show_info:
            font.render_to(
                window,
                text_margin,
                sim_name
            )
            font.render_to(
                window,
                text_margin + line_spacing,
                f"updates per second: {clock.get_fps():.0f}"
            )
            font.render_to(
                window,
                text_margin + line_spacing * 2,
                f"number of emitters: {len(sim.emitters)}"
            )
            font.render_to(
                window,
                text_margin + line_spacing * 3,
                f"number of particles: {len(sim.particles)}"
            )

        pygame.display.flip()
