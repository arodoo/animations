# Irrational names on the outer spiral arc.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ..domain.reveal import text_reveal, reveal_duration
from ..domain.spiral import pos, REAL_START, sz_at
from ..domain.motion import build_idle_bob

_NUMS = [
    'pi', 'e', 'v2', 'v3', 'v5',
    'v6', 'v7', 'v10', 'v11', 'v13',
    'phi', 'tau', 'gamma', 'ln2', 'ln3',
    'ln5', 'ln7', 'cbrt2', 'cbrt3', 'cbrt5',
    'e^2', 'e^3', 'pi^2', 'pi^3', '1/pi',
    '1/e', 'vpi', 've', 'e^pi', 'pi^e',
    'log23', 'log25', 'log32', 'log35', 'log53',
    'sin1', 'cos1', 'tan1', 'sin2', 'cos2',
    '2/vpi', 'v(2+v3)', 'v(3+v5)', 'v(5+v7)',
    'G', 'zeta3', 'delta', 'Omega', 'K',
    'A', 'B', 'lambda', 'mu', 'psi',
    'beta', 'log2e', 'log10e', 'logpi2',
    'e/pi', 'pi/e', '2^v2', 'v(1+v5)',
    'ln_pi', '1/v2', '1/v3', '1/phi',
    '3^(1/3)', 'v14', 'v15', 'v17', 'v19',
    'chi', 'rho', 'eta', 'theta', 'sigma',
    'kappa', 'xi', 'iota', 'alpha', 'nu',
    'digamma', 'v21', 'v22', 'v23', 'v26',
    'v29', 'v31', 'cbrt7', 'cbrt10', 'ln11',
    'ln13', 'ln17', 'sin3', 'cos3', 'tan2',
    'pi/4', 'v(7+v2)', 'e^(1/e)', 'pi*e',
    'v37', 'v41', 'v43', 'v47', 'zeta5',
    'zeta7', 'catalan', 'glaisher', 'v53',
    'v59', 'v61', 'v67', 'v71', 'v73',
    'v79', 'v83', 'v89', 'v97', 'ln19',
    'ln23', 'ln29', 'ln31', 'ln37',
    'ln41', 'ln43', 'ln47',
]
_STAGGER = reveal_duration()
_BOUNCE = 1.3
_TOTAL_FRAMES = 4800


def build_irrationals(
    appear_frame: int,
    base_sz: float = 0.75,
    total_frames: int = _TOTAL_FRAMES,
) -> List[Dict]:
    """120 irrationals, strictly sequential, pink."""
    cmds: List[Dict] = []
    for i, text in enumerate(_NUMS):
        x, y = pos(REAL_START + i)
        sz = sz_at(REAL_START + i, base_sz)
        f = appear_frame + i * _STAGGER
        cmds += text_reveal(
            f'Real{i}', text,
            x, y, 'MatReal', f,
            sz=sz, bounce=_BOUNCE,
            extrude=0.015,
        )
        cmds += build_idle_bob(
            f'Real{i}', x, y, f,
            total_frames, amplitude=0.02,
        )
    return cmds
