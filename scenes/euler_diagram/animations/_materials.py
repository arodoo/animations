# File: scenes/euler_diagram/animations/_materials.py
# Emissive materials for the Euler diagram.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_materials() -> List[Dict]:
    """Emissive materials for rings, numbers, labels."""
    return [
        {'cmd': 'create_material', 'args': {
            'name': 'MatInnerRing',
            'color': (0.8, 0.2, 1.0, 1.0),
            'emit': True,
            'emit_strength': 6.0,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'MatOuterRing',
            'color': (0.1, 0.6, 1.0, 1.0),
            'emit': True,
            'emit_strength': 6.0,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'MatOdds',
            'color': (1.0, 0.4, 1.0, 1.0),
            'emit': True,
            'emit_strength': 4.0,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'MatAll',
            'color': (0.4, 0.9, 1.0, 1.0),
            'emit': True,
            'emit_strength': 4.0,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'MatLabel',
            'color': (1.0, 1.0, 1.0, 1.0),
            'emit': True,
            'emit_strength': 2.5,
        }},
    ]
