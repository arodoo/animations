# Timing for the 5-act nautilus Euler diagram.
# All Rights Reserved Arodi Emmanuel

from typing import NamedTuple


class Timing(NamedTuple):
    """Frame offsets for each set's appearance."""
    odds_start: int = 60
    nat_start: int = 600
    int_start: int = 1500
    rat_start: int = 2400
    real_start: int = 3600
    finale: int = 4600
