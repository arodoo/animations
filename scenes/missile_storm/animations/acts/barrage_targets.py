# File: scenes/missile_storm/animations/acts/barrage_targets.py
# Target selection and stagger logic for barrage.
# All Rights Reserved Arodi Emmanuel

import random
from typing import Tuple

from ..domain.layout import VILLAGE_LAYOUT
from ..domain.timing import Timing

MISSILE_COUNT = 80
DESCENT_FRAMES = 50
_SPREAD = 900


def target_for(i: int) -> Tuple[float, float, float]:
    """Pick target: buildings first, random after."""
    if i < len(VILLAGE_LAYOUT):
        return VILLAGE_LAYOUT[i]['pos']
    rng = random.Random(i * 42)
    x = rng.uniform(-_SPREAD, _SPREAD)
    y = rng.uniform(-_SPREAD, _SPREAD)
    return (x, y, 0)


def stagger_frame(i: int, t: Timing) -> int:
    """Stagger missile arrival across barrage."""
    span = t.barrage_end - t.barrage_start
    return t.barrage_start + int(
        (i / MISSILE_COUNT) * span * 0.8,
    )
