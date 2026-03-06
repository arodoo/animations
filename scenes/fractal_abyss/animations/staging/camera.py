# Diving camera for Fractal Abyss.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from ..domain.timing import Timing

_STEP = 6
_RADIUS = 35.0
_FL = 50.0


def build_camera(
    total: int,
    timing: Timing,
) -> List[Dict]:
    """Camera orbits then dives into fractal."""
    nm = 'AbyssCam'
    cmds: List[Dict] = [
        {'cmd': 'create_camera', 'args': {
            'name': nm,
        }},
        {'cmd': 'set_focal_length', 'args': {
            'name': nm, 'focal_length': _FL,
        }},
    ]
    for f in range(1, total + 1, _STEP):
        t = (f - 1) / max(total - 1, 1)
        loc = _cam_pos(t, timing, total)
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': nm,
                'location': loc,
                'frame': f,
            },
        })
    cmds.append({
        'cmd': 'set_camera_target',
        'args': {'name': nm, 'target': (0, 0, 0)},
    })
    return cmds


def _cam_pos(t, timing, total):
    """Camera XYZ at normalized time t."""
    az = t * 3 * math.pi
    dive = max(0, t - timing.act4 / total)
    z = 40.0 - 30.0 * min(dive * 3, 1.0)
    r = _RADIUS * (1.0 - 0.4 * t)
    b = 0.15 * math.sin(t * 5 * math.pi)
    r *= (1.0 - b)
    el = math.atan2(z, r)
    d = math.sqrt(r * r + z * z)
    x = d * math.cos(el) * math.cos(az)
    y = d * math.cos(el) * math.sin(az)
    z_out = d * math.sin(el)
    return (x, y, z_out)
