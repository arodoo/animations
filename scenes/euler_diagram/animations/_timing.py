# File: scenes/euler_diagram/animations/_timing.py
# Timeline for the Expanding Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import NamedTuple


class Timing(NamedTuple):
    """Stage frame offsets for the Euler animation."""
    ring_inner: int = 60
    odds_appear: int = 120
    zoom_start: int = 250
    ring_outer: int = 380
    outer_nums: int = 440
    zoom_end: int = 560
    labels: int = 590
