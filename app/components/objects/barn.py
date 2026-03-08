# File: app/components/objects/barn.py
# Barn building: wide cube + tall cone roof.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_barn(
    name: str = 'Barn',
    pos: tuple = (0, 0, 0),
    size: float = 2.0,
) -> List[Dict]:
    """Spawn a barn (wide base + tall roof)."""
    bx, by, bz = pos
    s = size
    base = f'{name}_Base'
    roof = f'{name}_Roof'
    cmds: List[Dict] = []
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': base,
            'type': 'cube',
            'location': (bx, by, bz + s),
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': base,
            'scale': (s * 1.5, s * 2, s),
        },
    })
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': roof,
            'type': 'cone',
            'location': (
                bx, by, bz + s * 2.5,
            ),
            'radius1': s * 2.2,
            'depth': s * 1.5,
        },
    })
    cmds.append({
        'cmd': 'parent_object',
        'args': {
            'child': roof,
            'parent': base,
        },
    })
    cmds.append({
        'cmd': 'assign_material',
        'args': {
            'object': base,
            'material': 'MatBarnWood',
        },
    })
    cmds.append({
        'cmd': 'assign_material',
        'args': {
            'object': roof,
            'material': 'MatRoof',
        },
    })
    return cmds
