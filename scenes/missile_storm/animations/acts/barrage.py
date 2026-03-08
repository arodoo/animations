# File: scenes/missile_storm/animations/acts/barrage.py
# Act 3: 80 missiles rain down on the village.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from app.components.objects import (
    build_missile,
    build_explosion,
)
from ..domain.timing import Timing
from .barrage_targets import (
    MISSILE_COUNT,
    DESCENT_FRAMES,
    target_for,
    stagger_frame,
)


def build_barrage(
    timing: Timing,
) -> List[Dict]:
    """80 missiles descending + explosions."""
    cmds: List[Dict] = []
    for i in range(MISSILE_COUNT):
        name = f'Barrage{i}'
        target = target_for(i)
        tx, ty, tz = target
        hit_f = stagger_frame(i, timing)
        start_f = hit_f - DESCENT_FRAMES
        sx = tx + 30 * math.sin(i)
        sy = ty + 30 * math.cos(i)
        sz = 120 + (i % 5) * 20
        cmds += build_missile(
            name, (sx, sy, sz),
        )
        body = f'{name}_Body'
        cmds.append({
            'cmd': 'assign_material',
            'args': {
                'object': body,
                'material': 'MatMissile',
            },
        })
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': body,
                'location': (sx, sy, sz),
                'frame': max(1, start_f),
            },
        })
        cmds.append({
            'cmd': 'move_object',
            'args': {
                'name': body,
                'location': target,
                'frame': hit_f,
            },
        })
        cmds.append({
            'cmd': 'hide_at_frame',
            'args': {
                'name': body,
                'frame': hit_f,
            },
        })
        cmds += build_explosion(
            f'Exp{i}', target, hit_f,
            radius=8.0 + (i % 4) * 2,
            duration=40,
        )
    return cmds
