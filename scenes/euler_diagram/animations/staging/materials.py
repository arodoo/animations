# High-contrast emissive materials for visibility.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_DEFAULTS = {
    'odds':     {'color': (1.0, 0.95, 0.15), 'emit': 48.0},
    'naturals': {'color': (0.1, 1.00, 0.95), 'emit': 30.0},
    'integers': {'color': (0.6, 0.30, 1.00), 'emit': 34.0},
    'rationals': {'color': (0.2, 1.00, 0.40), 'emit': 30.0},
    'reals':    {'color': (1.0, 0.20, 0.70), 'emit': 34.0},
}


def _mat(name: str, rgb: tuple, strength: float) -> Dict:
    return {'cmd': 'create_material', 'args': {
        'name': name,
        'color': rgb + (1.0,),
        'emit': True,
        'emit_strength': strength,
    }}


def build_materials(
    sets: dict = None,
) -> List[Dict]:
    """High-emit materials; overridable per set."""
    s = {
        k: {**v, **(sets or {}).get(k, {})}
        for k, v in _DEFAULTS.items()
    }
    return [
        _mat('MatAxisX', (1.0, 0.15, 0.15), 8.0),
        _mat('MatAxisY', (0.15, 0.95, 0.25), 8.0),
        _mat(
            'MatOdds',
            s['odds']['color'],
            s['odds']['emit'],
        ),
        _mat(
            'MatNat',
            s['naturals']['color'],
            s['naturals']['emit'],
        ),
        _mat(
            'MatInt',
            s['integers']['color'],
            s['integers']['emit'],
        ),
        _mat(
            'MatRat',
            s['rationals']['color'],
            s['rationals']['emit'],
        ),
        _mat(
            'MatReal',
            s['reals']['color'],
            s['reals']['emit'],
        ),
    ]
