import argparse
import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

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

while True:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        emitter.handle_event(event)

    emitter.update(dt)

    emitter.draw(window)
    pygame.display.flip()
