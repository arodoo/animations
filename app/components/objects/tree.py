# File: app/components/objects/tree.py
# Simple tree: cylinder trunk + sphere canopy.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_tree(
    name: str = 'Tree',
    pos: tuple = (0, 0, 0),
    height: float = 3.0,
) -> List[Dict]:
    """Spawn a tree (trunk + canopy)."""
    tx, ty, tz = pos
    h = height
    trunk = f'{name}_Trunk'
    canopy = f'{name}_Canopy'
    cmds: List[Dict] = []
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': trunk,
            'type': 'cylinder',
            'location': (tx, ty, tz + h * 0.3),
            'radius': h * 0.06,
            'depth': h * 0.6,
        },
    })
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': canopy,
            'type': 'sphere',
            'location': (tx, ty, tz + h * 0.8),
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': canopy,
            'scale': (
                h * 0.3,
                h * 0.3,
                h * 0.35,
            ),
        },
    })
    cmds.append({
        'cmd': 'parent_object',
        'args': {
            'child': canopy,
            'parent': trunk,
        },
    })
    cmds.append({
        'cmd': 'assign_material',
        'args': {
            'object': trunk,
            'material': 'MatTrunk',
        },
    })
    cmds.append({
        'cmd': 'assign_material',
        'args': {
            'object': canopy,
            'material': 'MatCanopy',
        },
    })
    return cmds
