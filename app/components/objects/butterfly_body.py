# File: app/components/objects/butterfly_body.py
# Butterfly body from primitives (torso + head).
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_butterfly_body(
    name: str = 'Butterfly',
    pos: tuple = (0, 0, 3),
) -> List[Dict]:
    """Spawn butterfly torso + head."""
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
            'scale': (0.08, 0.25, 0.06),
        },
    })
    cmds.append({
        'cmd': 'spawn_primitive',
        'args': {
            'name': head,
            'type': 'sphere',
            'location': (bx, by + 0.3, bz),
        },
    })
    cmds.append({
        'cmd': 'scale_object',
        'args': {
            'name': head,
            'scale': (0.06, 0.06, 0.06),
        },
    })
    cmds.append({
        'cmd': 'parent_object',
        'args': {
            'child': head,
            'parent': torso,
        },
    })
    return cmds
