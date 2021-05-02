import pygame
import pygame.freetype

from src.bounce import BounceSystem
from src.default import DefaultSystem
from src.fire import FireSystem
from src.fireballs import FireballSystem


SYSTEMS = {
    "bounce": BounceSystem,
    "default": DefaultSystem,
    "fire": FireSystem,
    "fireballs": FireballSystem
}
SYSTEM_NAMES = sorted(list(SYSTEMS.keys()))


def run(system_name, window_size):
    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Particles")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    paused = False

    system = SYSTEMS[system_name]()
    system_index = SYSTEM_NAMES.index(system_name)

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
                    system.clear()
                elif event.key == pygame.K_n:
                    # Switch to the next system
                    system_index = (system_index + 1) % len(SYSTEM_NAMES)
                    system_name = SYSTEM_NAMES[system_index]
                    system = SYSTEMS[system_name]()
            system.handle_event(event)

        if not paused:
            system.update(dt, pygame.mouse.get_pos())

        system.draw(window)

        if show_info:
            font.render_to(
                window,
                text_margin,
                system_name
            )
            font.render_to(
                window,
                text_margin + line_spacing,
                f"updates per second: {clock.get_fps():.0f}"
            )
            font.render_to(
                window,
                text_margin + line_spacing * 2,
                f"number of particles: {len(system.particles)}"
            )
            if system_name == "fireballs":
                font.render_to(
                    window,
                    text_margin + line_spacing * 3,
                    f"number of emitters: {len(system.emitters)}"
                )

        pygame.display.flip()
