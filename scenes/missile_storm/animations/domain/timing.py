# File: scenes/missile_storm/animations/domain/timing.py
# Timing value object for butterfly meadow scene.
# All Rights Reserved Arodi Emmanuel

from typing import NamedTuple


class Timing(NamedTuple):
    """Frame markers (24 fps)."""
    flight_start: int = 1
    flight_end: int = 2880
