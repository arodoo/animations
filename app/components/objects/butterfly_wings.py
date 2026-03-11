# File: app/components/objects/butterfly_wings.py
# Butterfly wing pair with flapping keyframes.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List


def build_butterfly_wings(
    name: str = 'Butterfly',
    start_f: int = 1,
    end_f: int = 480,
    flap_speed: int = 4,
) -> List[Dict]:
    """Build wings + flap animation."""
    cmds: List[Dict] = []
    torso = f'{name}_Torso'
    for side, sx in (('L', 1), ('R', -1)):
        wn = f'{name}_Wing{side}'
        # LOCAL offset from torso center
        cmds.append({
            'cmd': 'spawn_primitive',
            'args': {
                'name': wn,
                'type': 'plane',
                'location': (sx * 1.0, 0, 0),
            },
        })
        cmds.append({
            'cmd': 'scale_object',
            'args': {
                'name': wn,
                'scale': (1.0, 0.85, 0.1),
            },
        })
        cmds.append({
            'cmd': 'parent_object',
            'args': {
                'child': wn,
                'parent': torso,
            },
        })
        for f in range(start_f, end_f + 1, flap_speed):
            t = (f - start_f) / max(1, end_f - start_f)
            angle = sx * 0.6 * math.sin(
                t * 80 * math.pi,
            )
            cmds.append({
                'cmd': 'rotate_object',
                'args': {
                    'name': wn,
                    'rotation': (0, angle, 0),
                    'frame': f,
                },
            })
    return cmds
