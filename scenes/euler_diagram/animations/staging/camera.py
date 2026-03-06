# Top-down zoom-out coordinated with 2400-frame timing.
# Camera distance tracks the outermost visible number.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

# Stages aligned to timing.py act starts.
# (frame, horiz_dist, height) — height/dist ratio ~1.6 = top-down feel
# Each stage frames the ring just filled by that act.
_STAGES = [
    (0,     7.0,  11.0),   # pre-roll: centered on r=4.44
    (48,    7.0,  11.0),   # odds: r ~ 4.4..5.3
    (348,  10.0,  16.0),   # naturals: r ~ 5.3..8.0
    (798,  14.5,  23.0),   # integers: r ~ 8.0..13.0
    (1248, 21.0,  33.0),   # rationals: r ~ 13..20
    (1698, 31.0,  49.0),   # reals: r ~ 20..30
    (2400, 36.0,  56.0),   # finale
]
# Gentle orbit: small horizontal sweep while zooming out
_BASE_ANGLE = math.pi / 4
_SWEEP = math.pi / 10


def _interp(frame: int):
    for i in range(len(_STAGES) - 1):
        f0, d0, h0 = _STAGES[i]
        f1, d1, h1 = _STAGES[i + 1]
        if f0 <= frame <= f1:
            t = (frame - f0) / (f1 - f0)
            return d0 + (d1 - d0) * t, h0 + (h1 - h0) * t
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
