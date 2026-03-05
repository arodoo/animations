# File: scenes/euler_diagram/animations/_camera.py
# Dramatic side-view zoom-out at low elevation.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

# (frame, horiz_dist, height) — elevation ~55°, scale=1.0
_STAGES = [
    (0,    14,  20),  # odds inner,   elev≈55°
    (540,  20,  29),  # naturals,     elev≈55°
    (1200, 32,  46),  # integers,     elev≈55°
    (1830, 50,  71),  # rationals,    elev≈55°
    (2460, 70,  100), # irrationals,  elev≈55°
    (2880, 76,  109), # finale hold
]
_BASE = math.pi / 4
_SWEEP = math.pi / 8


def _interp(frame: int, stages: list):
    """Linear interpolation between stage keypoints."""
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
    cam_start: tuple = None,
    cam_end: tuple = None,
) -> List[Dict]:
    """55°-elevation zoom-out — flat numbers readable from above."""
    stages = list(_STAGES)
    if cam_start:
        stages[0] = (_STAGES[0][0], *cam_start)
    if cam_end:
        stages[-1] = (_STAGES[-1][0], *cam_end)
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
