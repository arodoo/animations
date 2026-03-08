# File: scenes/missile_storm/animations/acts/flight_path.py
# Butterfly roaming flight path over the village.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing


def build_flight_path(
    timing: Timing,
    step: int = 2,
    radius: float = 600.0,
    altitude: float = 8.0,
) -> List[Dict]:
    """Animate butterfly roaming over village."""
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
        angle = p * 6 * math.pi
        r = radius * (
            0.3 + 0.7 * abs(math.sin(p * 3 * math.pi))
        )
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = altitude + 4 * math.sin(
            p * 12 * math.pi,
        )
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': 'Butterfly_Torso',
                'location': (x, y, z),
                'frame': f,
            },
        })
        dx = -math.sin(angle)
        dy = math.cos(angle)
        yaw = math.atan2(dy, dx)
        cmds.append({
            'cmd': 'rotate_object',
            'args': {
                'name': 'Butterfly_Torso',
                'rotation': (0, 0, yaw),
                'frame': f,
            },
        })
    return cmds
