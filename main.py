import argparse
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

import src.default


sims = {
    "default": src.default
}


def run(sim_name="default"):
    pygame.init()

    sim = sims[sim_name]
    window = pygame.display.set_mode(sim.WINDOW_SIZE)
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(sim.MOUSE_IS_VISIBLE)
    emitter = sim.Emitter()

    while True:
        dt = clock.tick(sim.FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            emitter.handle_event(event)

        emitter.update(dt)

        emitter.draw(window)
        pygame.display.flip()


run()
