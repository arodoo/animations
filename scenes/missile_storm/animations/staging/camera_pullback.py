# File: scenes/missile_storm/animations/staging/camera_pullback.py
# Camera pullback phase: dramatic zoom out over village.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing


def build_pullback_phase(
    t: Timing, step: int,
) -> List[Dict]:
    """Camera pulls back revealing village."""
    cmds: List[Dict] = []
    total = t.finale_end - t.pullback_start
    for f in range(
        t.pullback_start, t.finale_end, step,
    ):
        p = (f - t.pullback_start) / max(total, 1)
        alt = 10 + 600 * p * p
        dist = 50 + 1200 * p * p
        angle = p * 0.5 * math.pi
        cx = dist * math.cos(angle)
        cy = dist * math.sin(angle)
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': 'StormCam',
                'location': (cx, cy, alt),
                'frame': f,
            },
        })
    return cmds
