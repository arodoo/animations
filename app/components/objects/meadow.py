# File: app/components/objects/meadow.py
# Ground meadow plane with grass material.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_meadow(
    name: str = 'Meadow',
    size: float = 2000.0,
    pos: tuple = (0, 0, 0),
) -> List[Dict]:
    """Spawn a large ground plane for meadow."""
    mx, my, mz = pos
    cmds: List[Dict] = []
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': name,
            'type': 'plane',
            'location': (mx, my, mz),
            'size': size,
        },
    })
    cmds.append({
        'cmd': 'assign_material',
        'args': {
            'object': name,
            'material': 'MatGrass',
        },
    })
    return cmds
