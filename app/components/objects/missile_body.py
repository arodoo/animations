# File: app/components/objects/missile_body.py
# Missile from primitives (cylinder + cone nose).
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_missile(
    name: str = 'Missile',
    pos: tuple = (0, 0, 50),
) -> List[Dict]:
    """Spawn missile body + nose cone."""
    mx, my, mz = pos
    cmds: List[Dict] = []
    body = f'{name}_Body'
    nose = f'{name}_Nose'
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': body,
            'type': 'cylinder',
            'location': (mx, my, mz),
            'radius': 0.15,
            'depth': 2.0,
        },
    })
    cmds.append({
        'cmd': 'rotate_object',
        'args': {
            'name': body,
            'rotation': (1.5708, 0, 0),
        },
    })
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': nose,
            'type': 'cone',
            'location': (mx, my + 1.2, mz),
            'radius1': 0.15,
            'depth': 0.5,
        },
    })
    cmds.append({
        'cmd': 'rotate_object',
        'args': {
            'name': nose,
            'rotation': (1.5708, 0, 0),
        },
    })
    cmds.append({
        'cmd': 'parent_object',
        'args': {
            'child': nose,
            'parent': body,
        },
    })
    return cmds
