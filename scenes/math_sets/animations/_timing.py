# File: scenes/math_sets/animations/_timing.py
# Timeline configuration for the Math Sets proof animation.
# All Rights Reserved Arodi Emmanuel

from typing import NamedTuple


class Timing(NamedTuple):
    """Frame offsets for each act of the proof."""
    act1: int = 150   # N membership tags appear
    act2: int = 300   # Odds check tags appear
    act3: int = 450   # Venn rings reveal
    act4: int = 560   # Block migration
    act5: int = 700   # Formal proof text
