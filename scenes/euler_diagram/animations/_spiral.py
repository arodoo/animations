# File: scenes/euler_diagram/animations/_spiral.py
# Logarithmic (nautilus) spiral + angular-size scaling.
# All Rights Reserved Arodi Emmanuel

import math

TOTAL = 480
TURNS = 5.0
_ANGLE = TURNS * math.tau

_BASE_R_MIN = 5.8
_BASE_R_MAX = 69.0
_BASE_CAM_MIN = 28.0
_BASE_CAM_MAX = 143.0

R_MIN = _BASE_R_MIN
R_MAX = _BASE_R_MAX
_B = math.log(R_MAX / R_MIN) / _ANGLE
_CAM_MIN = _BASE_CAM_MIN
_CAM_MAX = _BASE_CAM_MAX


def configure(scale: float = 1.0):
    """Recompute spiral constants for the given scale."""
    global R_MIN, R_MAX, _B, _CAM_MIN, _CAM_MAX
    R_MIN = _BASE_R_MIN * scale
    R_MAX = _BASE_R_MAX * scale
    _B = math.log(R_MAX / R_MIN) / _ANGLE
    _CAM_MIN = _BASE_CAM_MIN * scale
    _CAM_MAX = _BASE_CAM_MAX * scale

# Global start indices per set
ODDS_START = 0    # 45 numbers: 0-44
NAT_START = 45    # 90 numbers: 45-134
INT_START = 135   # 120 numbers: 135-254
RAT_START = 255   # 150 numbers: 255-404
REAL_START = 405  # 75 numbers: 405-479


def pos(index: int):
    """(x, y) position for global spiral index."""
    theta = (index / TOTAL) * _ANGLE
    r = R_MIN * math.exp(_B * theta)
    return r * math.cos(theta), r * math.sin(theta)


def sz_at_r(r: float, base: float) -> float:
    """Scale base size for constant angular size at r."""
    t = max(0.0, min(1.0, (r - R_MIN) / (R_MAX - R_MIN)))
    cam = _CAM_MIN + t * (_CAM_MAX - _CAM_MIN)
    return base * math.sqrt(cam / _CAM_MIN)


def sz_at(index: int, base: float) -> float:
    """Scale base size for constant angular size at index."""
    theta = (index / TOTAL) * _ANGLE
    r = R_MIN * math.exp(_B * theta)
    return sz_at_r(r, base)
