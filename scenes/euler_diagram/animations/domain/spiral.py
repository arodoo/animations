# Logarithmic (nautilus) spiral with collision-free spacing.
# All Rights Reserved Arodi Emmanuel

import math

TOTAL = 720
TURNS = 6.5
_ANGLE = TURNS * math.tau

_BASE_R_MIN = 6.0
_BASE_R_MAX = 95.0
_BASE_CAM_MIN = 16.0
_BASE_CAM_MAX = 105.0

R_MIN = _BASE_R_MIN
R_MAX = _BASE_R_MAX
_B = math.log(R_MAX / R_MIN) / _ANGLE
_CAM_MIN = _BASE_CAM_MIN
_CAM_MAX = _BASE_CAM_MAX

ODDS_START = 0
NAT_START = 60
INT_START = 210
RAT_START = 390
REAL_START = 600


def configure(scale: float = 1.0):
    """Recompute spiral constants for given scale."""
    global R_MIN, R_MAX, _B, _CAM_MIN, _CAM_MAX
    R_MIN = _BASE_R_MIN * scale
    R_MAX = _BASE_R_MAX * scale
    _B = math.log(R_MAX / R_MIN) / _ANGLE
    _CAM_MIN = _BASE_CAM_MIN * scale
    _CAM_MAX = _BASE_CAM_MAX * scale


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
    """Scale for constant angular size at index."""
    r = radius_at(index)
    t = max(0.0, min(1.0, (r - R_MIN) / (R_MAX - R_MIN)))
    cam = _CAM_MIN + t * (_CAM_MAX - _CAM_MIN)
    return base * math.sqrt(cam / _CAM_MIN)


def sz_at_r(r: float, base: float) -> float:
    """Scale for constant angular size at radius r."""
    t = max(0.0, min(1.0, (r - R_MIN) / (R_MAX - R_MIN)))
    cam = _CAM_MIN + t * (_CAM_MAX - _CAM_MIN)
    return base * math.sqrt(cam / _CAM_MIN)
