# File: scenes/euler_diagram/animations/_spiral.py
# Logarithmic (nautilus) spiral + angular-size scaling.
# All Rights Reserved Arodi Emmanuel

import math

TOTAL = 480          # total numbers on spiral (3x)
TURNS = 5.0          # full rotations (more spacing)
_ANGLE = TURNS * math.tau
R_MIN = 2.5
R_MAX = 30.0
_B = math.log(R_MAX / R_MIN) / _ANGLE

# Camera distance bounds (mirrors _camera._STAGES)
_CAM_MIN = 12.0
_CAM_MAX = 62.0

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
