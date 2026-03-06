# Size-aware slot placement for the logarithmic spiral.
# All Rights Reserved Arodi Emmanuel

import math
from .spiral import radius_slot, display_sz, TOTAL_SLOTS, _ANGLE

_GAP = 1.4   # spacing multiplier between adjacent numbers


def slot_width(text) -> int:
    """Character count of label."""
    return max(1, len(str(text)))


def slots_advance(slot: int, text) -> int:
    """Slots to advance after placing text.

    Computes arc space the text physically occupies and converts
    to slot count, so numbers never overlap regardless of MIN_SZ.
    """
    chars = slot_width(text)
    arc = radius_slot(slot) * (_ANGLE / TOTAL_SLOTS)
    sz = display_sz(slot)
    return max(chars, math.ceil(chars * sz / arc * _GAP))
