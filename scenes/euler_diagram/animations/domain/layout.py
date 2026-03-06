# Size-aware slot placement for the logarithmic spiral.
# All Rights Reserved Arodi Emmanuel

import math
from .spiral import radius_slot, sz_at_slot, TOTAL_SLOTS, _ANGLE

_GAP = 1.4        # arc spacing multiplier
_GROWTH_STEP = 0.003   # size growth per global number index


def slot_width(text) -> int:
    """Character count of label."""
    return max(1, len(str(text)))


def slots_advance(slot: int, text) -> int:
    """Slots to advance after placing text.

    Uses unclamped arc size so inner-ring density stays compact
    while outer rings space naturally. Display size (MIN_SZ) and
    growth factor do not affect physical slot spacing.
    """
    chars = slot_width(text)
    arc = radius_slot(slot) * (_ANGLE / TOTAL_SLOTS)
    sz = sz_at_slot(slot)   # unclamped: sz/arc = 0.80 always
    return max(chars, math.ceil(chars * sz / arc * _GAP))
