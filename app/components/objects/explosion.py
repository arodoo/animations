# File: app/components/objects/explosion.py
# Explosion effect: expanding sphere + debris.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_explosion(
    name: str = 'Explosion',
    pos: tuple = (0, 0, 0),
    frame: int = 1,
    radius: float = 3.0,
    duration: int = 30,
) -> List[Dict]:
    """Spawn explosion sphere that scales up."""
    ex, ey, ez = pos
    cmds: List[Dict] = []
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': name,
            'type': 'sphere',
            'location': (ex, ey, ez),
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': name,
            'scale': (0.01, 0.01, 0.01),
            'frame': frame,
        },
    })
    peak = frame + duration // 3
    end = frame + duration
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': name,
            'scale': (radius, radius, radius),
            'frame': peak,
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': name,
            'scale': (0.01, 0.01, 0.01),
            'frame': end,
        },
    })
    cmds.append({
        'cmd': 'assign_material',
        'args': {
            'object': name,
            'material': 'MatExplosion',
        },
    })
    return cmds
