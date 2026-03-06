# Float bob: Z oscillation simulating hovering over a flat surface.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

# Bob height proportional to text size (passed from caller)
_PERIOD = 60   # frames per full cycle (~2.5s at 24fps)
_STEP   = 10   # keyframe every 10 frames


def build_idle_bob(
    name: str,
    x: float,
    y: float,
    appear_frame: int,
    total_frames: int,
    amplitude: float = 0.08,
) -> List[Dict]:
    """Sinusoidal Z float — text hovers like paper in breeze."""
    cmds: List[Dict] = []
    start = appear_frame + _PERIOD
    for f in range(start, total_frames, _STEP):
        t = (f - start) / _PERIOD
        z = amplitude * math.sin(t * math.tau)
        cmds.append({'cmd': 'move_object', 'args': {
            'name': name,
            'location': (x, y, z),
            'frame': f,
        }})
    return cmds
