# File: scenes/quasar_bh/animations/_black_hole.py
# Central black hole sphere — pure black, Schwarzschild-radius scaled.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_black_hole() -> List[Dict]:
    """Pure-black sphere scaled to the Schwarzschild radius."""
    from ._physics import SCHWARZSCHILD_RADIUS
    r_s = max(0.05, float(SCHWARZSCHILD_RADIUS))
    return [
        {'cmd': 'create_material', 'args': {
            'name': 'BlackHoleMat', 'color': (0, 0, 0, 1),
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'sphere', 'name': 'BlackHole',
            'segments': 64, 'ring_count': 32,
            'shade_smooth': True, 'subsurf_levels': 2,
        }},
        {'cmd': 'assign_material', 'args': {
            'object': 'BlackHole', 'material': 'BlackHoleMat',
        }},
        {'cmd': 'scale_object', 'args': {
            'name': 'BlackHole', 'scale': (r_s, r_s, r_s),
        }},
    ]
