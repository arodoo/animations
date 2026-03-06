# Logarithmic spiral with variable-width slots.
# Each number occupies len(str(text)) slots so wider
# numbers get proportionally more arc space — no overlap.
# All Rights Reserved Arodi Emmanuel

import math

# 335 total slots, 3 turns.
# R_MIN=4.44: arc_gap/slot=0.250 BU -> 1-digit sz=0.200 BU
# R_MAX=35.5: arc_gap/slot=2.000 BU -> 1-digit sz=1.600 BU
TOTAL_SLOTS = 335
TURNS = 3.0
_ANGLE = TURNS * math.tau

_BASE_R_MIN = 4.44
_BASE_R_MAX = 35.54

R_MIN = _BASE_R_MIN
R_MAX = _BASE_R_MAX
_B = math.log(R_MAX / R_MIN) / _ANGLE

# Slot starts per set (variable-width packing, gap=5 slots between sets)
# odds: 20 nums -> 35 slots; nat starts at 40
# nat:  30 nums -> 56 slots; int starts at 101
# int:  30 nums -> 81 slots; rat starts at 187
# rat:  30 nums -> 91 slots; real starts at 283
ODDS_START = 0
NAT_START = 40
INT_START = 101
RAT_START = 187
REAL_START = 283


def configure(scale: float = 1.0):
    """Recompute spiral for given scale."""
    global R_MIN, R_MAX, _B
    R_MIN = _BASE_R_MIN * scale
    R_MAX = _BASE_R_MAX * scale
    _B = math.log(R_MAX / R_MIN) / _ANGLE


def slot_width(text) -> int:
    """Slots consumed by one label (1 per char)."""
    return max(1, len(str(text)))


def pos_slot(slot: int):
    """(x, y, 0) for a slot index."""
    theta = (slot / TOTAL_SLOTS) * _ANGLE
    r = R_MIN * math.exp(_B * theta)
    return r * math.cos(theta), r * math.sin(theta), 0.0


def radius_slot(slot: int) -> float:
    """Radius at slot."""
    theta = (slot / TOTAL_SLOTS) * _ANGLE
    return R_MIN * math.exp(_B * theta)


def sz_at_slot(slot: int) -> float:
    """Glyph sz = 80% of one-slot arc gap."""
    r = radius_slot(slot)
    return r * (_ANGLE / TOTAL_SLOTS) * 0.80


def sz_at_r(r: float) -> float:
    """Glyph sz at explicit radius."""
    return r * (_ANGLE / TOTAL_SLOTS) * 0.80
