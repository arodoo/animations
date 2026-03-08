# File: scenes/missile_storm/animations/acts/strike_descent.py
# Missile descent animation toward a target.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_APPROACH_FRAMES = 40


def build_missile_descent(
    name: str,
    target: tuple,
    strike_f: int,
) -> List[Dict]:
    """Animate missile descending to target."""
    tx, ty, tz = target
    start_f = strike_f - _APPROACH_FRAMES
    cmds: List[Dict] = []
    body = f'{name}_Body'
    sx, sy, sz = tx + 20, ty - 30, 80
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
            'location': (tx, ty, tz),
            'frame': strike_f,
        },
    })
    cmds.append({
        'cmd': 'hide_object',
        'args': {'name': body},
    })
    return cmds
