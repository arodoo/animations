# File: scenes/euler_diagram/animations/_materials.py
# Eight emissive materials; each set has one color.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


_DEFAULTS = {
    'odds':      {'color': (1.0, 0.85, 0.00), 'emit': 28.0},
    'naturals':  {'color': (0.0, 1.00, 0.85), 'emit': 14.0},
    'integers':  {'color': (0.55, 0.0, 1.00), 'emit': 14.0},
    'rationals': {'color': (1.0, 0.45, 0.00), 'emit': 14.0},
    'reals':     {'color': (1.0, 0.10, 0.55), 'emit': 14.0},
}


def build_materials(sets: dict = None) -> List[Dict]:
    """Emissive materials; color+emit overridable per set."""
    s = {k: {**v, **(sets or {}).get(k, {})}
         for k, v in _DEFAULTS.items()}

    def m(name, rgb, strength):
        return {'cmd': 'create_material', 'args': {
            'name': name,
            'color': rgb + (1.0,),
            'emit': True,
            'emit_strength': strength,
        }}
    return [
        m('MatAxisX', (1.0, 0.10, 0.10),  6.0),
        m('MatAxisY', (0.10, 0.90, 0.20), 6.0),
        m('MatAxisZ', (0.0, 0.60, 1.00),  8.0),
        m('MatOdds', s['odds']['color'],      s['odds']['emit']),
        m('MatNat',  s['naturals']['color'],  s['naturals']['emit']),
        m('MatInt',  s['integers']['color'],  s['integers']['emit']),
        m('MatRat',  s['rationals']['color'], s['rationals']['emit']),
        m('MatReal', s['reals']['color'],     s['reals']['emit']),
    ]
