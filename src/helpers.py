"""Miscellaneous helper functions and classes."""


def linear_map(x, in_start=0, in_end=1, out_start=0, out_end=1):
    """
    Linearly map (scale) a number from one range to another range.
    Can also be used for linear interpolation. And you can invert
    the ranges by making start greater than end. Values outside
    both ranges are also possible.
    """
    return (x - in_start) / (in_end - in_start) * (out_end - out_start) + out_start


class Timer:
    def __init__(self, seconds, start_almost_full=True):
        self.delay = seconds
        self.initial_time = seconds - 0.000001 if start_almost_full else 0
        self.time = self.initial_time

    def update(self, dt):
        self.time += dt
        if self.time >= self.delay:
            n, self.time = divmod(self.time, self.delay)
            return int(n)
        return 0

    def reset(self):
        self.time = self.initial_time
