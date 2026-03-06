# Timing for the 5-act nautilus Euler diagram.
# All Rights Reserved Arodi Emmanuel

from typing import NamedTuple


class Timing(NamedTuple):
    """Frame offsets — 2400 total, 130 numbers at stagger=15f.

    odds:  20 nums, frames   48-348  (14.5s)
    nat:   30 nums, frames  348-798  (18.8s)
    int:   30 nums, frames  798-1248 (18.8s)
    rat:   30 nums, frames 1248-1698 (18.8s)
    real:  20 nums, frames 1698-1998 (12.5s)
    """
    odds_start: int = 48
    nat_start: int = 348
    int_start: int = 798
    rat_start: int = 1248
    real_start: int = 1698
    finale: int = 2100
