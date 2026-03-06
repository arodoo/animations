# Gentle drift/bob animation for floating objects.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

_STEP = 12
_PERIOD = 72


def build_drift(
    name: str,
    x: float,
    y: float,
    z: float,
    start: int,
    end: int,
    amp: float = 0.1,
) -> List[Dict]:
    """Sinusoidal Z bob for floating objects."""
    cmds: List[Dict] = []
    for f in range(start, end, _STEP):
        t = (f - start) / _PERIOD
        dz = amp * math.sin(t * math.tau)
        cmds.append({'cmd': 'move_object', 'args': {
            'name': name,
            'location': (x, y, z + dz),
            'frame': f,
        }})
    return cmds
