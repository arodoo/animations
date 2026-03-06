# Act 4: Sierpinski fractal pattern forms.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.text_spawner import (
    spawn_glow_text,
)
from app.components.number_drift import build_drift
from app.components.fractal_layout import sierpinski

_DEPTH = 3
_SIZE = 18.0
_STAG = 16
_SZ = 0.35
_MAT = 'MatFrac'
_SYMS = [
    'N', 'Z', 'Q', 'R', 'C',
    '0', '1', 'i', 'e', 'pi',
]


def build_fractal(
    start: int,
    total: int,
) -> List[Dict]:
    """27 Sierpinski triangle markers."""
    cmds: List[Dict] = []
    pts = sierpinski(0, 0, _SIZE, _DEPTH)
    n = len(_SYMS)
    for i, (x, y) in enumerate(pts):
        nm = f'Frac{i}'
        sym = _SYMS[i % n]
        f = start + i * _STAG
        cmds += spawn_glow_text(
            nm, sym, x, y, 0.0,
            _MAT, f, sz=_SZ, ext=0.03,
        )
        cmds += build_drift(
            nm, x, y, 0.0,
            f + 36, total, amp=0.06,
        )
    return cmds
