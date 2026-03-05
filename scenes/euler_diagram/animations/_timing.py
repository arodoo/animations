# File: scenes/euler_diagram/animations/_timing.py
# Timeline for the 5-act nautilus Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import NamedTuple


class Timing(NamedTuple):
    """Frame offsets for each set's appearance."""
    odds_start: int = 60     # Act 1 – odds (stagger 10f)
    nat_start: int = 540     # Act 2 – naturals (stagger 7f)
    int_start: int = 1200    # Act 3 – integers (stagger 5f)
    rat_start: int = 1830    # Act 4 – rationals (stagger 4f)
    real_start: int = 2460   # Act 5 – irrationals (stagger 3f)
    finale: int = 2720       # spiral complete
