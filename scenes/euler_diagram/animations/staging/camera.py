# Top-down zoom-out coordinated with 2400-frame timing.
# Camera distance tracks the outermost visible number.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

# Stages aligned to timing.py act starts.
# Distances are 40% larger than visual minimum to always lead the spiral.
# (frame, horiz_dist, height)
_STAGES = [
    (0,     5.6,   8.4),   # pre-roll
    (48,    5.6,   8.4),   # odds
    (348,   8.4,  13.3),   # naturals
    (798,  13.3,  21.0),   # integers
    (1248, 21.0,  33.6),   # rationals
    (1698, 33.6,  53.2),   # reals
    (2400, 42.0,  64.4),   # finale
]
# Gentle orbit: small horizontal sweep while zooming out
_BASE_ANGLE = math.pi / 4
_SWEEP = math.pi / 10


def _exp_lerp(a: float, b: float, t: float) -> float:
    """Exponential interpolation — matches logarithmic spiral growth."""
    return math.exp(math.log(a) * (1.0 - t) + math.log(b) * t)


def _interp(frame: int):
    for i in range(len(_STAGES) - 1):
        f0, d0, h0 = _STAGES[i]
        f1, d1, h1 = _STAGES[i + 1]
        if f0 <= frame <= f1:
            t = (frame - f0) / (f1 - f0)
            return _exp_lerp(d0, d1, t), _exp_lerp(h0, h1, t)
    return _STAGES[-1][1], _STAGES[-1][2]


def build_camera(
    total_frames: int,
    scale: float = 1.0,
) -> List[Dict]:
    """Smooth top-down zoom-out over the spiral."""
    cmds: List[Dict] = [
        {'cmd': 'create_camera', 'args': {'name': 'SceneCamera'}},
        {'cmd': 'set_focal_length', 'args': {
            'name': 'SceneCamera', 'focal_length': 50.0,
        }},
        {'cmd': 'set_camera_target', 'args': {
            'name': 'SceneCamera', 'target': (0, 0, 0),
        }},
    ]
    for f in range(1, total_frames + 1, 6):
        dist, h = _interp(f)
        t = f / total_frames
        angle = _BASE_ANGLE + t * _SWEEP
        cx = dist * scale * math.cos(angle)
        cy = dist * scale * math.sin(angle)
        cmds.append({'cmd': 'move_object', 'args': {
            'name': 'SceneCamera',
            'location': (cx, cy, h * scale),
            'frame': f,
        }})
    return cmds
