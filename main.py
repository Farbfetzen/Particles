import argparse
import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame.freetype  # imports also pygame

import src.default
import src.fire
import src.bounce


parser = argparse.ArgumentParser()
parser.add_argument(
    "name",
    nargs="?",
    default="default",
    help="Name of the particle simulation."
)
parser.add_argument(
    "-w",
    "--window-size",
    metavar=("<width>", "<height>"),
    nargs=2,
    type=int,
    default=(1200, 800),
    help="Specify the window width and height in pixels."
)
args = parser.parse_args()

sims = {
    "default": src.default,
    "fire": src.fire,
    "bounce": src.bounce
}
if args.name not in sims:
    parser.error(f"name must be one of {list(sims.keys())}")
sim = sims[args.name]


pygame.init()
window = pygame.display.set_mode(args.window_size)
pygame.display.set_caption("Particles")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
emitter = sim.Emitter()

show_info = True
font = pygame.freetype.SysFont("inconsolate, consolas, monospace", 16)
# invert background color but not the alpha value
font.fgcolor = pygame.Color([255 - x for x in sim.BACKGROUND_COLOR[:3]])
line_spacing = pygame.Vector2(0, font.get_sized_height())
text_margin = pygame.Vector2(5, 5)

paused = False

while True:
    dt = clock.tick(60) / 1000  # in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_F1:
                show_info = not show_info
            elif event.key == pygame.K_SPACE:
                paused = not paused
                pygame.mouse.set_visible(paused)
            elif event.key == pygame.K_DELETE:
                emitter.particles.clear()
        emitter.handle_event(event)

    if not paused:
        emitter.update(dt)

    emitter.draw(window)
    if show_info:
        font.render_to(
            window,
            text_margin,
            f"updates per second: {clock.get_fps():.0f}"
        )
        font.render_to(
            window,
            text_margin + line_spacing,
            f"number of particles: {len(emitter.particles)}"
        )
    pygame.display.flip()
