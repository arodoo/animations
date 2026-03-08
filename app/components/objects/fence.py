# File: app/components/objects/fence.py
# Fence section from a thin cube.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_fence(
    name: str = 'Fence',
    pos: tuple = (0, 0, 0),
    length: float = 5.0,
    rotation_z: float = 0.0,
) -> List[Dict]:
    """Spawn a fence section."""
    fx, fy, fz = pos
    cmds: List[Dict] = []
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': name,
            'type': 'cube',
            'location': (fx, fy, fz + 0.5),
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': name,
            'scale': (
                length * 0.5,
                0.05,
                0.5,
            ),
        },
    })
    if rotation_z != 0.0:
        cmds.append({
            'cmd': 'rotate_object',
            'args': {
                'name': name,
                'rotation': (0, 0, rotation_z),
            },
        })
    cmds.append({
        'cmd': 'assign_material',
        'args': {
            'object': name,
            'material': 'MatFence',
        },
    })
    return cmds
