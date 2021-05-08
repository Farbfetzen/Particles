# Inspired by the portals in the movie Doctor Strange


import pygame

from src.base import System, Emitter, Particle


class PortalSystem(System):
    def __init__(self):
        super().__init__(0)


class PortalEmitter(Emitter):
    # Maybe one or multiple emitters spinning around?
    pass


class PortalParticle(Particle):
    # Maybe drawn as lines? From the current position
    # backwards using the velocity vector?
    pass
