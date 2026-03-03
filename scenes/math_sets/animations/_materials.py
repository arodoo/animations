# File: scenes/math_sets/animations/_materials.py
# Materials for the Math Sets implication proof.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def generate_math_materials() -> List[Dict]:
    """Materials for sets and logical states."""
    return [
        {'cmd': 'create_material', 'args': {
            'name': 'EvenMat',
            'color': (0.1, 0.2, 0.4, 1.0),
            'roughness': 0.2,
            'emit': True,
            'emit_strength': 0.8,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'OddMat',
            'color': (1.0, 0.55, 0.0, 1.0),
            'roughness': 0.2,
            'emit': True,
            'emit_strength': 4.0,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'TextMat',
            'color': (1.0, 1.0, 1.0, 1.0),
            'roughness': 0.8,
            'emit': True,
            'emit_strength': 1.5,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'TrueMat',
            'color': (0.0, 0.9, 0.3, 1.0),
            'roughness': 0.5,
            'emit': True,
            'emit_strength': 3.0,
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'FalseMat',
            'color': (1.0, 0.1, 0.1, 1.0),
            'roughness': 0.5,
            'emit': True,
            'emit_strength': 3.0,
        }},
    ]
