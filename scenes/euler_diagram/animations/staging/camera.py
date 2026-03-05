# Top-down zoom-out matching spiral R_MIN=3.5..R_MAX=18.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

# (frame, horiz_dist, height)
# At each stage the camera views the current act's ring.
_STAGES = [
    (0,     4.5,  6.5),  # odds: r~3.5..4
    (600,   7,   10),    # naturals: r~4..6
    (1500, 11,   15),    # integers: r~6..10
    (2400, 15,   21),    # rationals: r~10..14
    (3600, 20,   27),    # irrationals: r~14..18
    (4800, 23,   31),    # finale
]
_BASE = math.pi / 4
_SWEEP = math.pi / 6


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
