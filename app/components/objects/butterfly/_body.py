# File: app/components/objects/butterfly/_body.py
# Private: torso, head, antennae commands.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_body(
    name: str,
    pos: tuple,
) -> List[Dict]:
    """Spawn torso + head + antennae."""
    bx, by, bz = pos
    torso = f'{name}_Torso'
    head = f'{name}_Head'
    cmds: List[Dict] = [
        {'cmd': 'spawn_primitive', 'args': {
            'name': torso, 'type': 'sphere',
            'location': (bx, by, bz),
        }},
        {'cmd': 'scale_object', 'args': {
            'name': torso,
            'scale': (0.22, 0.72, 0.22),
        }},
        {'cmd': 'apply_scale', 'args': {
            'name': torso,
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'name': head, 'type': 'sphere',
            'location': (0, 0.82, 0.08),
        }},
        {'cmd': 'scale_object', 'args': {
            'name': head,
            'scale': (0.22, 0.22, 0.22),
        }},
        {'cmd': 'parent_object', 'args': {
            'child': head, 'parent': torso,
        }},
    ]
    for side, sx in (('L', 1), ('R', -1)):
        an = f'{name}_Antenna{side}'
        cmds += [
            {'cmd': 'spawn_primitive', 'args': {
                'name': an, 'type': 'cylinder',
                'location': (sx * 0.1, 1.1, 0.15),
                'radius': 0.02, 'depth': 0.5,
            }},
            {'cmd': 'rotate_object', 'args': {
                'name': an,
                'rotation': (0.5, sx * 0.3, 0),
            }},
            {'cmd': 'parent_object', 'args': {
                'child': an, 'parent': torso,
            }},
        ]
    return cmds
