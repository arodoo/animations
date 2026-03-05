# File: scenes/euler_diagram/animations/_materials.py
# Eight emissive materials; each set has one color.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_materials() -> List[Dict]:
    """Bright saturated colors for dark background."""
    def m(name, c, s):
        return {'cmd': 'create_material', 'args': {
            'name': name,
            'color': c + (1.0,),
            'emit': True,
            'emit_strength': s,
        }}
    return [
        m('MatAxisX', (1.0, 0.10, 0.10),  6.0),
        m('MatAxisY', (0.10, 0.90, 0.20), 6.0),
        m('MatAxisZ', (0.0, 0.60, 1.00),  8.0),
        m('MatOdds', (1.0, 0.85, 0.00),  28.0),  # GOLD x2
        m('MatNat',  (0.0, 1.00, 0.85),  14.0),  # TEAL
        m('MatInt',  (0.55, 0.0, 1.00),  14.0),  # VIOLET
        m('MatRat',  (1.0, 0.45, 0.00),  14.0),  # ORANGE
        m('MatReal', (1.0, 0.10, 0.55),  14.0),  # HOT PINK
    ]
