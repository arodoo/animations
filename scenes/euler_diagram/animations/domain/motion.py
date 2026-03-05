# Idle Z-oscillation for number liveliness.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List


def build_idle_bob(
    name: str,
    x: float,
    y: float,
    appear_frame: int,
    total_frames: int,
    amplitude: float = 0.15,
    period: int = 90,
) -> List[Dict]:
    """Subtle up-down oscillation after appearing."""
    cmds: List[Dict] = []
    step = max(period // 4, 8)
    start = appear_frame + 30
    for f in range(start, total_frames, step):
        t = (f - start) / period
        z = amplitude * math.sin(t * math.tau)
        cmds.append({'cmd': 'move_object', 'args': {
            'name': name,
            'location': (x, y, z),
            'frame': f,
        }})
    return cmds
