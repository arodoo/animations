# File: scenes/math_sets/animations/_materials.py
# Materials designating mathematical realities (Evens, Odds, Typography).
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def generate_math_materials() -> List[Dict]:
    """Return materials that differentiate mathematical sets."""
    return [
        {'cmd': 'create_material', 'args': {
            'name': 'EvenMat',
            'color': (0.1, 0.15, 0.2, 1.0), # Cold, dim steel for evens
            'roughness': 0.1,
            'emit': True,
            'emit_strength': 0.1, # Barely visible
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'OddMat',
            'color': (1.0, 0.5, 0.0, 1.0), # Brilliant golden/orange for odds
            'roughness': 0.3,
            'emit': True,
            'emit_strength': 5.0, # Highly visible
        }},
        {'cmd': 'create_material', 'args': {
            'name': 'TextMat',
            'color': (1.0, 1.0, 1.0, 1.0), # Pure white for readable math
            'roughness': 0.8,
            'emit': True,
            'emit_strength': 1.5,
        }},
    ]
