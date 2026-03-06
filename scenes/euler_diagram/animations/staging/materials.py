# Emission materials for Euler diagram sets and labels.
# Numbers: emit=30. Labels: emit=60 (same hue, higher intensity).

from typing import Dict, List

_COLORS: Dict[str, tuple] = {
    'odds':      (1.00, 0.92, 0.05, 1.0),
    'naturals':  (0.05, 1.00, 0.85, 1.0),
    'integers':  (0.65, 0.20, 1.00, 1.0),
    'rationals': (0.10, 1.00, 0.30, 1.0),
    'reals':     (1.00, 0.10, 0.55, 1.0),
}

_NUM_EMIT: Dict[str, float] = {
    'odds': 30.0, 'naturals': 30.0, 'integers': 30.0,
    'rationals': 30.0, 'reals': 30.0,
}
_LBL_EMIT = 60.0

_MAT_MAP = {
    'odds': 'MatOdds', 'naturals': 'MatNat',
    'integers': 'MatInt', 'rationals': 'MatRat', 'reals': 'MatReal',
}
_LBL_MAP = {
    'odds': 'MatLblOdds', 'naturals': 'MatLblNat',
    'integers': 'MatLblInt', 'rationals': 'MatLblRat',
    'reals': 'MatLblReal',
}


def build_materials(
    overrides: Dict[str, float] | None = None,
) -> List[Dict]:
    """create_material commands for number sets."""
    ovr = overrides or {}
    cmds: List[Dict] = []
    for key, color in _COLORS.items():
        emit = ovr.get(key, _NUM_EMIT[key])
        cmds.append({'cmd': 'create_material', 'args': {
            'name': _MAT_MAP[key],
            'color': color,
            'emission_strength': emit,
        }})
    return cmds


def build_label_materials() -> List[Dict]:
    """Bright label materials — same hues, 2× emission."""
    return [
        {'cmd': 'create_material', 'args': {
            'name': _LBL_MAP[key],
            'color': color,
            'emission_strength': _LBL_EMIT,
        }}
        for key, color in _COLORS.items()
    ]


def mat_name(key: str) -> str:
    return _MAT_MAP[key]


def lbl_mat_name(key: str) -> str:
    return _LBL_MAP[key]
