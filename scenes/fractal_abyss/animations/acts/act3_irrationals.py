# Act 3: Irrationals pierce through from edges.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from app.components.text_spawner import (
    spawn_glow_text,
)

_IRRS = [
    'pi', 'e', 'sqrt2', 'phi',
    'sqrt3', 'sqrt5', 'ln2',
    'sqrt7', 'pi/2', 'e^2',
]
_STAG = 48
_SZ = 0.55
_MAT = 'MatIrr'
_R = 12.0
_IN_DUR = 120
_IN_STEP = 8


def build_irrationals(
    start: int,
    total: int,
) -> List[Dict]:
    """10 irrationals spiral from outer ring."""
    cmds: List[Dict] = []
    n = len(_IRRS)
    for i, sym in enumerate(_IRRS):
        nm = f'Irr{i}'
        a = i * math.tau / n
        x = _R * math.cos(a)
        y = _R * math.sin(a)
        f = start + i * _STAG
        cmds += spawn_glow_text(
            nm, sym, x, y, 0.0,
            _MAT, f, sz=_SZ, ext=0.05,
        )
        cmds += _spiral_in(nm, x, y, f, total)
    return cmds


def _spiral_in(nm, x0, y0, start, total):
    """Spiral object inward with rotation."""
    cmds = []
    end = min(start + _IN_DUR, total)
    for f in range(start, end, _IN_STEP):
        t = (f - start) / _IN_DUR
        e = t * t * (3 - 2 * t)
        cx = x0 * (1 - e * 0.6)
        cy = y0 * (1 - e * 0.6)
        a = e * math.pi
        cs, sn = math.cos(a), math.sin(a)
        rx = cx * cs - cy * sn
        ry = cx * sn + cy * cs
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': nm,
                'location': (rx, ry, 0.0),
                'frame': f,
            },
        })
    return cmds
