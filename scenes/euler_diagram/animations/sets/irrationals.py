# Irrational names on the outer spiral arc.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal, reveal_duration
from ..domain.spiral import pos, REAL_START, sz_at
from ..domain.motion import build_idle_bob

_NUMS = [
    'π', 'e', '√2', '√3', '√5',
    'φ', 'τ', 'γ', 'ln2', 'ln3',
    '√7', 'cbrt2', 'e²', 'π²', '1/π',
    'e^π', 'π^e', '2^√2', '√φ', 'ζ(3)',
]
_STAGGER = 15
_BOUNCE = 1.3
_TOTAL_FRAMES = 2400


def build_irrationals(
    appear_frame: int,
    base_sz: float = 1.0,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """20 iconic irrationals, sequential, pink."""
    cmds: List[Dict] = []
    for i, text in enumerate(_NUMS):
        x, y = pos(REAL_START + i)
        sz = sz_at(REAL_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Real{i}', text,
            x, y, 'MatReal', f,
            sz=sz, bounce=_BOUNCE,
            extrude=0.012,
        )
        cmds += build_idle_bob(
            f'Real{i}', x, y, f,
            total_frames, amplitude=0.02,
        )
    return cmds
