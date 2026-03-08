# File: app/components/objects/house.py
# Simple house: cube base + cone roof.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_house(
    name: str = 'House',
    pos: tuple = (0, 0, 0),
    size: float = 1.0,
) -> List[Dict]:
    """Spawn a house (base + roof)."""
    hx, hy, hz = pos
    s = size
    base = f'{name}_Base'
    roof = f'{name}_Roof'
    cmds: List[Dict] = []
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': base,
            'type': 'cube',
            'location': (hx, hy, hz + s),
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': base,
            'scale': (s, s * 1.2, s),
        },
    })
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': roof,
            'type': 'cone',
            'location': (
                hx, hy, hz + s * 2.3,
            ),
            'radius1': s * 1.5,
            'depth': s * 1.2,
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
            'material': 'MatHouseWall',
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
