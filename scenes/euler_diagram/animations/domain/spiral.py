# Logarithmic (nautilus) spiral — self-consistent proportions.
# All Rights Reserved Arodi Emmanuel

import math

# 720 slots, 4.5 turns.
# R_MIN=3.5: inner arc_gap = 3.5*(4.5*2pi/720) = 0.137 BU
# Text floor=0.12 BU → ratio ~1.14 ✔
# Camera start: dist=6, h=9 → cam_dist~11 BU
# Text angular size: 0.12/11 ≈ 0.6° -- supplemented by bloom
TOTAL = 720
TURNS = 4.5
_ANGLE = TURNS * math.tau

_BASE_R_MIN = 3.5
_BASE_R_MAX = 18.0

R_MIN = _BASE_R_MIN
R_MAX = _BASE_R_MAX
_B = math.log(R_MAX / R_MIN) / _ANGLE

ODDS_START = 0
NAT_START = 60
INT_START = 210
RAT_START = 390
REAL_START = 600


def configure(scale: float = 1.0):
    """Recompute spiral constants for given scale."""
    global R_MIN, R_MAX, _B
    R_MIN = _BASE_R_MIN * scale
    R_MAX = _BASE_R_MAX * scale
    _B = math.log(R_MAX / R_MIN) / _ANGLE


def pos(index: int):
    """(x, y) for global spiral index."""
    theta = (index / TOTAL) * _ANGLE
    r = R_MIN * math.exp(_B * theta)
    return r * math.cos(theta), r * math.sin(theta)


def radius_at(index: int) -> float:
    """Spiral radius at index."""
    theta = (index / TOTAL) * _ANGLE
    return R_MIN * math.exp(_B * theta)


def sz_at(index: int, base: float) -> float:
    """Text size: 75% of local arc gap.
    Emission bloom compensates at inner radii."""
    r = radius_at(index)
    arc_gap = r * (_ANGLE / TOTAL)
    return arc_gap * 0.75 * base


def sz_at_r(r: float, base: float) -> float:
    """Text size at radius r."""
    arc_gap = r * (_ANGLE / TOTAL)
    return arc_gap * 0.75 * base
