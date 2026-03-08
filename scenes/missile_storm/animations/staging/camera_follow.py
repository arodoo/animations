# File: scenes/missile_storm/animations/staging/camera_follow.py
# Camera follows butterfly from behind and above.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing

_CAM_BACK = 12
_CAM_UP = 5
_LOOK_AHEAD = 5
_RADIUS = 600.0
_ALT = 8.0


def _butterfly_pos(p: float):
    """Butterfly world position at progress p."""
    angle = p * 6 * math.pi
    r = _RADIUS * (
        0.3 + 0.7 * abs(
            math.sin(p * 3 * math.pi)
        )
    )
    x = r * math.cos(angle)
    y = r * math.sin(angle)
    z = _ALT + 4 * math.sin(
        p * 12 * math.pi,
    )
    dx = -math.sin(angle)
    dy = math.cos(angle)
    return x, y, z, dx, dy


def build_follow_phase(
    t: Timing, step: int,
) -> List[Dict]:
    """Camera + target track butterfly."""
    cmds: List[Dict] = []
    total = t.flight_end - t.flight_start
    for f in range(t.flight_start, t.flight_end, step):
        p = (f - t.flight_start) / max(total, 1)
        bx, by, bz, dx, dy = _butterfly_pos(p)
        cx = bx - dx * _CAM_BACK
        cy = by - dy * _CAM_BACK
        cz = bz + _CAM_UP
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': 'StormCam',
                'location': (cx, cy, cz),
                'frame': f,
            },
        })
        tx = bx + dx * _LOOK_AHEAD
        ty = by + dy * _LOOK_AHEAD
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': '_target_StormCam',
                'location': (tx, ty, bz),
                'frame': f,
            },
        })
    return cmds
