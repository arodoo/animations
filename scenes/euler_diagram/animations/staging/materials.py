# High-contrast emissive materials for visibility.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

_DEFAULTS = {
    'odds':      {'color': (1.0,  0.92, 0.10), 'emit': 5.0},
    'naturals':  {'color': (0.10, 1.00, 0.85), 'emit': 4.0},
    'integers':  {'color': (0.55, 0.25, 1.00), 'emit': 4.5},
    'rationals': {'color': (0.15, 1.00, 0.35), 'emit': 4.0},
    'reals':     {'color': (1.0,  0.15, 0.60), 'emit': 4.5},
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
