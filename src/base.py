from abc import ABC, abstractmethod


class Emitter(ABC):

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self, target_surface):
        pass


class Particle:

    @abstractmethod
    def update(self, dt, forces):
        pass
