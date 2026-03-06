# Logarithmic spiral — starts near origin, opens outward.
# All Rights Reserved Arodi Emmanuel

import math

# 200 slots, 3 turns.
# R_MIN=2.3: first number appears close to 0,0,0
# R_MAX=11.5: ratio 5x gives clear visual expansion
# arc_gap_inner=0.214 BU → text=0.15 BU → 1.05° at cam dist 8
TOTAL = 200
TURNS = 3.0
_ANGLE = TURNS * math.tau

_BASE_R_MIN = 2.3
_BASE_R_MAX = 11.5

R_MIN = _BASE_R_MIN
R_MAX = _BASE_R_MAX
_B = math.log(R_MAX / R_MIN) / _ANGLE

# Slot assignments — gaps between sets for visual breathing room
ODDS_START = 0
NAT_START = 25
INT_START = 60
RAT_START = 95
REAL_START = 130


def configure(scale: float = 1.0):
    """Recompute spiral constants for given scale."""
    global R_MIN, R_MAX, _B
    R_MIN = _BASE_R_MIN * scale
    R_MAX = _BASE_R_MAX * scale
    _B = math.log(R_MAX / R_MIN) / _ANGLE


def pos(index: int):
    """(x, y) for global spiral slot index."""
    theta = (index / TOTAL) * _ANGLE
    r = R_MIN * math.exp(_B * theta)
    return r * math.cos(theta), r * math.sin(theta)


def radius_at(index: int) -> float:
    """Spiral radius at slot index."""
    theta = (index / TOTAL) * _ANGLE
    return R_MIN * math.exp(_B * theta)


def sz_at(index: int, base: float) -> float:
    """Text size: 70% of local arc gap, min 0.15 BU."""
    r = radius_at(index)
    arc_gap = r * (_ANGLE / TOTAL)
    return max(arc_gap * 0.70 * base, 0.15 * base)


def sz_at_r(r: float, base: float) -> float:
    """Text size at radius r."""
    arc_gap = r * (_ANGLE / TOTAL)
    return max(arc_gap * 0.70 * base, 0.15 * base)
