import pygame
import pygame.freetype


def run(systems, system_name, window_size):
    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Particles")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    paused = False

    system = systems[system_name]()
    system_names = sorted(list(systems.keys()))
    system_index = system_names.index(system_name)

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
                    system_index = (system_index + 1) % len(system_names)
                    system_name = system_names[system_index]
                    system = systems[system_name]()
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
