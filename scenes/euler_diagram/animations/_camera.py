# File: scenes/euler_diagram/animations/_camera.py
# Dramatic side-view zoom-out at low elevation.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

# (frame, horiz_dist, height) — elevation ~55°, 2.3x spiral scale
_STAGES = [
    (0,    28,  40),  # odds inner,   elev≈55°
    (540,  41,  59),  # naturals,     elev≈55°
    (1200, 64,  92),  # integers,     elev≈55°
    (1830, 97, 138),  # rationals,    elev≈55°
    (2460, 133, 191), # irrationals,  elev≈55°
    (2880, 143, 205), # finale hold
]
_BASE = math.pi / 4
_SWEEP = math.pi / 8


def _interp(frame: int):
    """Linear interpolation between stage keypoints."""
    for i in range(len(_STAGES) - 1):
        f0, d0, h0 = _STAGES[i]
        f1, d1, h1 = _STAGES[i + 1]
        if f0 <= frame <= f1:
            t = (frame - f0) / (f1 - f0)
            return (
                d0 + (d1 - d0) * t,
                h0 + (h1 - h0) * t,
            )
    return _STAGES[-1][1], _STAGES[-1][2]


def build_camera(
    total_frames: int,
    scale: float = 1.0,
) -> List[Dict]:
    """55°-elevation zoom-out — flat numbers readable from above."""
    cmds: List[Dict] = [
        {'cmd': 'create_camera',
         'args': {'name': 'SceneCamera'}},
        {'cmd': 'set_focal_length', 'args': {
            'name': 'SceneCamera',
            'focal_length': 70.0}},
        {'cmd': 'set_camera_target', 'args': {
            'name': 'SceneCamera',
            'target': (0, 0, 0)}},
    ]
    for f in range(1, total_frames + 1, 15):
        dist, h = _interp(f)
        t = f / total_frames
        angle = _BASE + t * _SWEEP
        cx = dist * scale * math.cos(angle)
        cy = dist * scale * math.sin(angle)
        cmds.append({'cmd': 'move_object', 'args': {
            'name': 'SceneCamera',
            'location': (cx, cy, h * scale),
            'frame': f,
        }})
    return cmds
