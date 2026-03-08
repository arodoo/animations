# File: scenes/missile_storm/animations/domain/timing.py
# Timing value object for missile storm acts.
# All Rights Reserved Arodi Emmanuel

from typing import NamedTuple


class Timing(NamedTuple):
    """Frame markers for each act (24 fps)."""
    flight_start: int = 1
    flight_end: int = 480
    strike_frame: int = 481
    strike_explode: int = 500
    pullback_start: int = 500
    barrage_start: int = 600
    barrage_end: int = 1080
    finale_end: int = 1200
