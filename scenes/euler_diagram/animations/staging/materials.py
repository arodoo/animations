# Emission materials for Euler diagram sets.
# Bright saturated colors on dark background.
# emit=8-12 range: visible without bloom blowout.

from typing import Dict, List

_DEFS: Dict[str, Dict] = {
    'odds':      {'color': (1.00, 0.92, 0.05, 1.0), 'emit': 10.0},
    'naturals':  {'color': (0.05, 1.00, 0.85, 1.0), 'emit':  9.0},
    'integers':  {'color': (0.65, 0.20, 1.00, 1.0), 'emit':  9.0},
    'rationals': {'color': (0.10, 1.00, 0.30, 1.0), 'emit':  9.0},
    'reals':     {'color': (1.00, 0.10, 0.55, 1.0), 'emit':  9.0},
}

_MAT_MAP = {
    'odds':      'MatOdds',
    'naturals':  'MatNat',
    'integers':  'MatInt',
    'rationals': 'MatRat',
    'reals':     'MatReal',
}


def build_materials(
    overrides: Dict[str, float] | None = None,
) -> List[Dict]:
    """Return create_material commands for all sets."""
    emit_ovr = overrides or {}
    cmds: List[Dict] = []
    for key, defs in _DEFS.items():
        emit = emit_ovr.get(key, defs['emit'])
        cmds.append({'cmd': 'create_material', 'args': {
            'name': _MAT_MAP[key],
            'color': defs['color'],
            'emission_strength': emit,
        }})
    return cmds


def mat_name(key: str) -> str:
    return _MAT_MAP[key]
