# File: scenes/missile_storm/animations/acts/first_strike.py
# Act 2: First missile hits butterfly and explodes.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List

from app.components.objects import (
    build_missile,
    build_missile_trail,
    build_explosion,
)
from ..domain.timing import Timing
from .strike_descent import build_missile_descent


def _butterfly_pos_at(t: Timing) -> tuple:
    """Butterfly position at strike frame."""
    total = t.flight_end - t.flight_start
    p = (t.strike_frame - t.flight_start) / max(
        total, 1,
    )
    x = p * 200 - 100
    y = 30 * math.sin(p * 4 * math.pi)
    z = 3 + math.sin(p * 6 * math.pi)
    return (x, y, z)


def build_first_strike(
    timing: Timing,
) -> List[Dict]:
    """Act 2: missile + impact + explosion."""
    cmds: List[Dict] = []
    target = _butterfly_pos_at(timing)
    cmds += build_missile('Strike0', (0, 0, 80))
    cmds += build_missile_trail('Strike0')
    for obj, mat in [
        ('Strike0_Body', 'MatMissile'),
        ('Strike0_Nose', 'MatMissileNose'),
    ]:
        cmds.append({
            'cmd': 'assign_material',
            'args': {
                'object': obj,
                'material': mat,
            },
        })
    cmds += build_missile_descent(
        'Strike0', target, timing.strike_frame,
    )
    cmds += build_explosion(
        'Explosion0',
        target,
        timing.strike_explode,
        radius=5.0,
    )
    cmds.append({
        'cmd': 'hide_object',
        'args': {'name': 'Butterfly_Torso'},
    })
    return cmds
