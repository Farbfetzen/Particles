import argparse
import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame.freetype  # imports also pygame

from src.helpers import EventTimer
import src.default
import src.fire


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
    "fire": src.fire
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

show_info = False
font = pygame.freetype.SysFont("inconsolate, consolas, monospace", 16)
# invert background color but not the alpha value
font.fgcolor = pygame.Color([255 - x for x in sim.BACKGROUND_COLOR[:3]])
line_spacing = pygame.Vector2(0, font.get_sized_height())
text_margin = pygame.Vector2(5, 5)

# Separate updates (ups) from draw updates (fps). More updates per frame means
# a smoother emission pattern. Otherwise there may be visible puffs
# of particles when the emitter is moving quickly across the window.
UPS = 120
FPS = 60
DRAW_EVENT_ID = pygame.event.custom_type()
draw_timer = EventTimer(DRAW_EVENT_ID, 1 / FPS, True)
draw = False
paused = False

while True:
    dt = clock.tick(UPS) / 1000  # in seconds
    draw_timer.update(dt)

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
        elif event.type == DRAW_EVENT_ID:
            draw = True
        emitter.handle_event(event)

    if not paused:
        emitter.update(dt)

    if draw:
        draw = False
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
