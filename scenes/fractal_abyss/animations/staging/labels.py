# Set labels for Fractal Abyss acts.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.text_spawner import (
    spawn_glow_text,
)
from ..domain.timing import Timing

_SZ = 1.5
_EXT = 0.12

_LABELS = [
    ('LblNat', 'N', -12, 10),
    ('LblRat', 'Q', 12, 10),
    ('LblIrr', 'R\\Q', -12, -10),
    ('LblFrac', 'Fractal', 12, -10),
    ('LblAby', 'Abyss', 0, -14),
]


def build_labels(timing: Timing) -> List[Dict]:
    """Spawn set labels at each act start."""
    frames = [
        timing.act1 + 24,
        timing.act2 + 24,
        timing.act3 + 24,
        timing.act4 + 24,
        timing.act5 + 24,
    ]
    cmds: List[Dict] = []
    for i, (nm, txt, x, y) in enumerate(_LABELS):
        cmds += spawn_glow_text(
            nm, txt, x, y, 0.5,
            'MatLabel', frames[i],
            sz=_SZ, ext=_EXT,
        )
    return cmds
