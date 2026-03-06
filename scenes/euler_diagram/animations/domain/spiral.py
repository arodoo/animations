# Logarithmic spiral with variable-width slots.
# Each number consumes slots proportional to display size.
# All Rights Reserved Arodi Emmanuel

import math

# 700 total slots, 3 turns.
# R_MIN=1.5 BU: first number near origin.
# R_MAX=35.0 BU: ratio ~23x across 3 turns.
# MIN_SZ: absolute physical size — does NOT scale with spiral.
TOTAL_SLOTS = 700
TURNS = 3.0
_ANGLE = TURNS * math.tau

_BASE_R_MIN = 1.5
_BASE_R_MAX = 35.0
_BASE_MIN_SZ = 0.12

R_MIN = _BASE_R_MIN
R_MAX = _BASE_R_MAX
MIN_SZ = _BASE_MIN_SZ
_B = math.log(R_MAX / R_MIN) / _ANGLE

# Slot starts per set (size-aware packing, gap=10 slots between sets).
# Computed for 20 odds / 30 nat / 30 int / 30 rat / 20 real.
ODDS_START = 0
NAT_START  = 145
INT_START  = 275
RAT_START  = 390
REAL_START = 550


def configure(scale: float = 1.0):
    """Recompute spiral for given scale."""
    global R_MIN, R_MAX, MIN_SZ, _B
    R_MIN = _BASE_R_MIN * scale
    R_MAX = _BASE_R_MAX * scale
    MIN_SZ = _BASE_MIN_SZ        # absolute physical size, not scaled
    _B = math.log(R_MAX / R_MIN) / _ANGLE


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
    """Arc-based glyph size (no clamp, for geometry checks)."""
    r = radius_slot(slot)
    return r * (_ANGLE / TOTAL_SLOTS) * 0.80


def sz_at_r(r: float) -> float:
    """Arc-based glyph size at explicit radius."""
    return r * (_ANGLE / TOTAL_SLOTS) * 0.80


def display_sz(slot: int) -> float:
    """Visible glyph size: clamped to MIN_SZ so inner glyphs are readable."""
    return max(sz_at_slot(slot), MIN_SZ)


def display_sz_r(r: float) -> float:
    """Visible glyph size at explicit radius."""
    return max(sz_at_r(r), MIN_SZ)
