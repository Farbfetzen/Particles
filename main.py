import argparse
import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame.freetype

import src.default


sims = {
    "default": src.default
}
sim = sims["default"]


pygame.init()
window = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Particles")
clock = pygame.time.Clock()
pygame.mouse.set_visible(sim.MOUSE_IS_VISIBLE)
emitter = sim.Emitter()

show_info = False
font = pygame.freetype.SysFont("inconsolate, consolas, monospace", 16)
# invert background color but not the alpha value
font.fgcolor = pygame.Color([255 - x for x in sim.BACKGROUND_COLOR[:3]])
print(font.fgcolor)
line_spacing = pygame.Vector2(0, font.get_sized_height())
text_margin = pygame.Vector2(5, 5)

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_F1:
                show_info = not show_info
        emitter.handle_event(event)

    emitter.update(dt)

    emitter.draw(window)

    if show_info:
        font.render_to(
            window,
            text_margin,
            f"fps: {clock.get_fps():.0f}"
        )
        font.render_to(
            window,
            text_margin + line_spacing,
            f"number of particles: {len(emitter.particles)}"
        )

    pygame.display.flip()
