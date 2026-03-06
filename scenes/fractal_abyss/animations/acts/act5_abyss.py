# Act 5: Infinite descent into the abyss.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.text_spawner import (
    spawn_glow_text,
)
from app.components.number_drift import build_drift
from app.components.fractal_layout import sierpinski

_DEPTH = 3
_SIZE = 6.0
_STAG = 12
_SZ = 0.25
_MAT = 'MatAbyss'
_SYMS = [
    '...', 'inf', '0.0', '1/n',
    'dx', 'lim', 'sum', 'int',
    'n!', 'n^n',
]

_FINALS = [
    ('Fin0', '...', 0, 3),
    ('Fin1', 'INFINITY', 3, -2),
    ('Fin2', '???', -3, -2),
]


def build_abyss(
    start: int,
    total: int,
) -> List[Dict]:
    """Inner fractal layer + final symbols."""
    cmds: List[Dict] = []
    pts = sierpinski(0, 0, _SIZE, _DEPTH)
    n = len(_SYMS)
    for i, (x, y) in enumerate(pts):
        nm = f'Aby{i}'
        f = start + i * _STAG
        if f >= total:
            break
        cmds += spawn_glow_text(
            nm, _SYMS[i % n], x, y, -0.5,
            _MAT, f, sz=_SZ, ext=0.02,
        )
        cmds += build_drift(
            nm, x, y, -0.5,
            f + 24, total, amp=0.05,
        )
    cmds += _final_symbols(start + 300, total)
    return cmds


def _final_symbols(start, total):
    """Prominent closing symbols."""
    cmds = []
    for nm, txt, x, y in _FINALS:
        if start >= total:
            break
        cmds += spawn_glow_text(
            nm, txt, x, y, -1.0,
            'MatLabel', start,
            sz=0.8, ext=0.08,
        )
    return cmds
