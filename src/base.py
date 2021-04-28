class Simulation:
    def __init__(self):
        pass

    def handle_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, dt):
        pass


class Emitter:
    # Handles particle emission but does not store them. Particles are stored,
    # updated and drawn in the Simulation object.
    def __init__(self):
        pass

    def emit(self):
        pass


class Particle:
    def __init__(self):
        pass

    def update(self, dt):
        pass
