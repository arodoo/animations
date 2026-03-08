# File: scenes/missile_storm/animations/staging/camera_follow.py
# Camera follow phase: tracks butterfly from behind.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing


def build_follow_phase(
    t: Timing, step: int,
) -> List[Dict]:
    """Camera follows butterfly from behind."""
    cmds: List[Dict] = []
    for f in range(
        t.flight_start, t.flight_end, step,
    ):
        p = (f - 1) / max(t.flight_end - 1, 1)
        bx = p * 200 - 100
        by = 30 * math.sin(p * 4 * math.pi)
        bz = 3 + math.sin(p * 6 * math.pi)
        cx = bx - 8
        cy = by - 3
        cz = bz + 2
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': 'StormCam',
                'location': (cx, cy, cz),
                'frame': f,
            },
        })
    return cmds
