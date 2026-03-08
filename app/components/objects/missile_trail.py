# File: app/components/objects/missile_trail.py
# Missile smoke/fire trail via particle system.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_missile_trail(
    name: str = 'Missile',
    count: int = 200,
    lifetime: int = 30,
) -> List[Dict]:
    """Add smoke trail particles to missile."""
    body = f'{name}_Body'
    return [{
        'cmd': 'add_particle_system',
        'args': {
            'object': body,
            'name': f'{name}_Trail',
            'count': count,
            'lifetime': lifetime,
            'emit_from': 'FACE',
            'normal_factor': -0.5,
            'gravity': 0.1,
            'size': 0.08,
            'render_type': 'HALO',
        },
    }]
