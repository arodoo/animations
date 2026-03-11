# File: app/components/objects/butterfly_body.py
# Butterfly body: torso, head, antennae.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_butterfly_body(
    name: str = 'Butterfly',
    pos: tuple = (0, 0, 3),
) -> List[Dict]:
    """Spawn torso + head + antennae."""
    bx, by, bz = pos
    cmds: List[Dict] = []
    torso = f'{name}_Torso'
    head = f'{name}_Head'
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': torso,
            'type': 'sphere',
            'location': (bx, by, bz),
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': torso,
            'scale': (0.22, 0.72, 0.22),
        },
    })
    cmds.append({
        'cmd': 'apply_scale',
        'args': {'name': torso},
    })
    # Head at LOCAL offset from torso
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': head,
            'type': 'sphere',
            'location': (0, 0.82, 0.08),
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': head,
            'scale': (0.22, 0.22, 0.22),
        },
    })
    cmds.append({
        'cmd': 'parent_object',
        'args': {'child': head, 'parent': torso},
    })
    for side, sx in (('L', 1), ('R', -1)):
        an = f'{name}_Antenna{side}'
        cmds.append({
            'cmd': 'spawn_primitive',
            'args': {
                'name': an, 'type': 'cylinder',
                'location': (sx * 0.1, 1.1, 0.15),
                'radius': 0.02, 'depth': 0.5,
            },
        })
        cmds.append({
            'cmd': 'rotate_object',
            'args': {
                'name': an,
                'rotation': (0.5, sx * 0.3, 0),
            },
        })
        cmds.append({
            'cmd': 'parent_object',
            'args': {'child': an, 'parent': torso},
        })
    return cmds
