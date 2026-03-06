# Emission materials for Euler diagram sets.
# Numbers emit=30 for high visibility on dark background.

from typing import Dict, List

_COLORS: Dict[str, tuple] = {
    'odds':      (1.00, 0.92, 0.05, 1.0),
    'naturals':  (0.05, 1.00, 0.85, 1.0),
    'integers':  (0.65, 0.20, 1.00, 1.0),
    'rationals': (0.10, 1.00, 0.30, 1.0),
    'reals':     (1.00, 0.10, 0.55, 1.0),
}

_EMIT: Dict[str, float] = {
    'odds': 30.0, 'naturals': 30.0, 'integers': 30.0,
    'rationals': 30.0, 'reals': 30.0,
}

_MAT_MAP = {
    'odds': 'MatOdds', 'naturals': 'MatNat',
    'integers': 'MatInt', 'rationals': 'MatRat', 'reals': 'MatReal',
}


def build_materials(
    overrides: Dict[str, float] | None = None,
) -> List[Dict]:
    """create_material commands for all number sets."""
    ovr = overrides or {}
    cmds: List[Dict] = []
    for key, color in _COLORS.items():
        emit = ovr.get(key, _EMIT[key])
        cmds.append({'cmd': 'create_material', 'args': {
            'name': _MAT_MAP[key],
            'color': color,
            'emission_strength': emit,
        }})
    return cmds


def mat_name(key: str) -> str:
    return _MAT_MAP[key]
