# File: scenes/math_sets/animations/_proof_text.py
# Act 5: formal logical proof of Odds subset N.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Tuple

_LINES: List[Tuple[str, float, str]] = [
    ("Odds is a SUBSET of N",    6.0, 'OddMat'),
    ("x in Odds  =>  x in N",   5.0, 'TrueMat'),
    ("x in N  =/=>  x in Odds", 4.0, 'FalseMat'),
    ("Proof: 2 in N, 2 not Odds", 3.0, 'FalseMat'),
]


def generate_proof_statements(
    reveal_frame: int
) -> List[Dict]:
    """Reveal each proof line with a 25-frame stagger."""
    cmds: List[Dict] = []
    for i, (text, z, mat) in enumerate(_LINES):
        name = f"Proof_{i}"
        frame = reveal_frame + i * 25
        cmds.append({'cmd': 'spawn_text', 'args': {
            'name': name, 'text': text,
            'location': (0.0, 0.0, z),
            'extrude': 0.04,
            'align_x': 'CENTER',
            'align_y': 'BOTTOM',
        }})
        cmds.append({'cmd': 'assign_material', 'args': {
            'object': name, 'material': mat,
        }})
        cmds.append({'cmd': 'scale_object', 'args': {
            'name': name,
            'scale': (0, 0, 0),
            'frame': 1,
        }})
        cmds.append({'cmd': 'scale_object', 'args': {
            'name': name,
            'scale': (1.0, 1.0, 1.0),
            'frame': frame,
        }})
    return cmds
