"""Miscellaneous helper functions and classes."""

import pygame


def linear_map(x, in_start, in_end, out_start=0, out_end=1):
    """
    Linearly map (scale) a number from one range to another range.
    Can also be used for linear interpolation. And you can invert
    the ranges by making start greater than end. Values outside
    both ranges are also possible.
    """
    return (x - in_start) / (in_end - in_start) * (out_end - out_start) + out_start


class Timer:
    def __init__(self, seconds):
        """
        A simple timer. It differs from EventTimer in that it doesn't
        post events to the event queue and instead returns the number
        of events since the previous update.
        :param seconds: The time between events in seconds.
        """
        self.delay = seconds
        self.time = 0

    def update(self, dt):
        """
        Update the timer and post the event if it is time to do so.
        :param dt: The delta time in seconds.
        :return: The number of events since the previous update.
        """
        self.time += dt
        if self.time >= self.delay:
            n, self.time = divmod(self.time, self.delay)
            return int(n)
        return 0


class EventTimer:
    def __init__(self, eventid, seconds, once=False):
        """
        Works like pygame.time.set_event() with these differences:
          - can use floats for the time
          - uses seconds instead of milliseconds
        Caution: Don't spam the event queue! It can only hold a certain number of events.
        :param eventid: Event id, ideally created by pygame.event.custom_type().
        :param seconds: The time between events in seconds.
        :param once: Send the event only once per update.
        """
        self.event = pygame.event.Event(eventid)
        self.delay = seconds
        self.once = once
        self.time = 0

    def update(self, dt):
        """
        Update the timer and post the event if it is time to do so.
        :param dt: The delta time in seconds.
        :return: None
        """
        self.time += dt
        if self.time >= self.delay:
            n, self.time = divmod(self.time, self.delay)
            if self.once:
                pygame.event.post(self.event)
            else:
                for _ in range(int(n)):
                    pygame.event.post(self.event)
