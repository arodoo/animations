# File: scenes/missile_storm/animations/acts/flight_path.py
# Butterfly sinusoidal flight path keyframes.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing


def build_flight_path(
    timing: Timing, step: int = 2,
) -> List[Dict]:
    """Animate butterfly along sinusoidal path."""
    cmds: List[Dict] = []
    total = timing.flight_end - timing.flight_start
    for f in range(
        timing.flight_start,
        timing.flight_end,
        step,
    ):
        p = (f - timing.flight_start) / max(
            total, 1,
        )
        x = p * 200 - 100
        y = 30 * math.sin(p * 4 * math.pi)
        z = 3 + math.sin(p * 6 * math.pi)
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': 'Butterfly_Torso',
                'location': (x, y, z),
                'frame': f,
            },
        })
        yaw = math.atan2(
            math.cos(p * 4 * math.pi) * 4,
            1.0,
        )
        cmds.append({
            'cmd': 'rotate_object',
            'args': {
                'name': 'Butterfly_Torso',
                'rotation': (0, 0, yaw),
                'frame': f,
            },
        })
    return cmds
