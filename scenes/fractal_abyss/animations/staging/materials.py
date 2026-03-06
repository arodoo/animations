# Emission materials for Fractal Abyss.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_MATS: Dict[str, tuple] = {
    'MatNat': (0.3, 0.7, 1.0, 1.0),
    'MatRat': (0.1, 1.0, 0.4, 1.0),
    'MatIrr': (1.0, 0.1, 0.6, 1.0),
    'MatFrac': (1.0, 0.85, 0.1, 1.0),
    'MatAbyss': (1.0, 0.05, 0.15, 1.0),
    'MatLabel': (1.0, 1.0, 1.0, 1.0),
}

_EMIT = 30.0


def build_materials() -> List[Dict]:
    """Create all glow materials."""
    cmds: List[Dict] = []
    for name, color in _MATS.items():
        cmds.append({
            'cmd': 'create_material',
            'args': {
                'name': name,
                'color': color,
                'emit': True,
                'emit_strength': _EMIT,
            },
        })
    return cmds
