# Dramatic zoom-out camera at 55° elevation.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

_STAGES = [
    (0,    14,  20),
    (600,  22,  31),
    (1500, 38,  54),
    (2400, 56,  80),
    (3600, 78, 112),
    (4800, 86, 123),
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
    """55°-elevation zoom-out for flat spiral."""
    stages = list(_STAGES)
    cmds: List[Dict] = [
        {'cmd': 'create_camera',
         'args': {'name': 'SceneCamera'}},
        {'cmd': 'set_focal_length', 'args': {
            'name': 'SceneCamera',
            'focal_length': 70.0,
        }},
        {'cmd': 'set_camera_target', 'args': {
            'name': 'SceneCamera',
            'target': (0, 0, 0),
        }},
    ]
    for f in range(1, total_frames + 1, 15):
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
