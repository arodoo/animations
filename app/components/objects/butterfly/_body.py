# File: app/components/objects/butterfly/_body.py
# Private: torso, head, antennae commands.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_SD = (1.06, 0.94, 1.06)  # downstroke: compact/effort
_SU = (0.97, 1.04, 0.97)  # upstroke: graceful stretch


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


def build_body_dynamics(
    name: str,
    start_f: int,
    end_f: int,
    half_cycle: int,
) -> List[Dict]:
    """Squash+stretch torso synced to wingbeat (#1)."""
    torso = f'{name}_Torso'
    cmds: List[Dict] = []
    up, f = False, start_f
    while f <= end_f:
        s = _SU if up else _SD
        cmds.append({'cmd': 'scale_object', 'args': {
            'name': torso, 'frame': f, 'scale': s,
        }})
        up, f = not up, f + half_cycle
    return cmds
