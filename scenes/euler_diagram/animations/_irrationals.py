# File: scenes/euler_diagram/animations/_irrationals.py
# 75 irrational names on the outer spiral arc.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._helpers import text_reveal
from ._spiral import pos, REAL_START, sz_at

_NUMS = [
    'pi', 'e', 'v2', 'v3', 'v5',
    'v6', 'v7', 'v10', 'v11', 'v13',
    'phi', 'tau', 'gamma', 'ln2', 'ln3',
    'ln5', 'ln7', 'cbrt2', 'cbrt3', 'cbrt5',
    'e^2', 'e^3', 'pi^2', 'pi^3', '1/pi',
    '1/e', 'vpi', 've', 'e^pi', 'pi^e',
    'log23', 'log25', 'log32', 'log35', 'log53',
    'sin1', 'cos1', 'tan1', 'sin2', 'cos2',
    '2/vpi', 'v(2+v3)', 'v(3+v5)', 'v(5+v7)', 'G',
    'zeta3', 'delta', 'Omega', 'K', 'A',
    'B', 'lambda', 'mu', 'psi', 'beta',
    'log2e', 'log10e', 'logpi2', 'e/pi', 'pi/e',
    '2^v2', 'v(1+v5)', 'ln_pi', '1/v2', '1/v3',
    '1/phi', '3^(1/3)', 'v14', 'v15', 'v17',
    'v19', 'chi', 'rho', 'eta', 'theta',
]
_BASE_SZ = 0.70
_STAGGER = 3
_BOUNCE = 1.3


def build_irrationals(
    appear_frame: int,
    base_sz: float = _BASE_SZ,
) -> List[Dict]:
    """75 irrationals, stagger 3f, hot pink."""
    cmds: List[Dict] = []
    for i, text in enumerate(_NUMS):
        x, y = pos(REAL_START + i)
        sz = sz_at(REAL_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Real{i}', text,
            x, y, 'MatReal', f,
            sz=sz, bounce=_BOUNCE,
        )
    return cmds
