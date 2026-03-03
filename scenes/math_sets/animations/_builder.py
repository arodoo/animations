# File: scenes/math_sets/animations/_builder.py
# Orchestrates the 5-act Odds-subset-of-N proof.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._materials import generate_math_materials
from ._number_row import build_number_row
from ._equations import build_membership_acts
from ._logic_blocks import build_all_migrations
from ._venn_diagram import generate_set_rings
from ._proof_text import generate_proof_statements
from ._kinematics import build_kinematics
from ._post_sort import build_post_sort
from ._timing import Timing


def build_math_sets(
    total_frames: int,
    num_sequence: int = 10,
    timing: Timing = None,
) -> List[Dict]:
    """
    Proves: Odds subset N, but N not subset Odds.
    Act 1 (t.act1): Numbers appear, each tagged 'in N'.
    Act 2 (t.act2): Each tested for 'in Odds' (T/F).
    Act 3 (t.act3): Venn rings reveal the set structure.
    Act 4 (t.act4): Blocks fly into correct ring regions.
    Act 5 (t.act5): Formal logical proof statements.
    """
    t = timing or Timing()
    cmds: List[Dict] = generate_math_materials()
    cmds += build_number_row(num_sequence)
    cmds += build_membership_acts(
        num_sequence, t.act1, t.act2,
    )
    cmds += generate_set_rings(t.act3)
    cmds += build_all_migrations(num_sequence, t.act4)
    cmds += build_kinematics(
        num_sequence, total_frames, t.act4, t.act3,
    )
    cmds += build_post_sort(
        num_sequence, t.act4, total_frames,
    )
    if total_frames >= t.act5:
        cmds += generate_proof_statements(t.act5)
    return cmds
