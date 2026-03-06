# Top-down zoom-out — coordinated with 2400-frame timing.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

# Stages align with act starts from timing.py
# (frame, horiz_dist, height) — h/dist ratio ~1.6 keeps top-down feel
_STAGES = [
    (0,    3.5,  5.5),   # pre-roll: close on origin
    (48,   3.5,  5.5),   # odds: r ~ 2.3..3.2
    (348,  5.5,  8.5),   # naturals: r ~ 3.2..5.0
    (798,  7.5, 12.0),   # integers: r ~ 5.0..7.2
    (1248, 10.5, 16.5),  # rationals: r ~ 7.2..9.5
    (1698, 14.0, 22.0),  # reals: r ~ 9.5..11.5
    (2400, 16.0, 25.0),  # finale
]
_BASE = math.pi / 4
_SWEEP = math.pi / 8


def _interp(frame: int, stages: list):
    """Linear interpolation between camera stages."""
    for i in range(len(stages) - 1):
        f0, d0, h0 = stages[i]
        f1, d1, h1 = stages[i + 1]
        if f0 <= frame <= f1:
            t = (frame - f0) / (f1 - f0)
            return (
                d0 + (d1 - d0) * t,
                h0 + (h1 - h0) * t,
            )
    return stages[-1][1], stages[-1][2]


def build_camera(
    total_frames: int,
    scale: float = 1.0,
) -> List[Dict]:
    """Top-down zoom-out over the spiral."""
    stages = list(_STAGES)
    cmds: List[Dict] = [
        {'cmd': 'create_camera',
         'args': {'name': 'SceneCamera'}},
        {'cmd': 'set_focal_length', 'args': {
            'name': 'SceneCamera',
            'focal_length': 50.0,
        }},
        {'cmd': 'set_camera_target', 'args': {
            'name': 'SceneCamera',
            'target': (0, 0, 0),
        }},
    ]
    for f in range(1, total_frames + 1, 12):
        dist, h = _interp(f, stages)
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
