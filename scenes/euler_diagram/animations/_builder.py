# File: scenes/euler_diagram/animations/_builder.py
# Orchestrates all sub-builders for the Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._timing import Timing
from ._materials import build_materials
from ._spiral import configure as _configure_spiral
from ._background import build_background
from ._odds import build_odds
from ._naturals import build_naturals
from ._integers import build_integers
from ._rationals import build_rationals
from ._irrationals import build_irrationals
from ._labels import build_labels


def build_euler_diagram(
    total_frames: int,
    timing: Timing = None,
    spiral_scale: float = 1.0,
    sets: dict = None,
    label_size: float = 1.60,
) -> List[Dict]:
    """Build all commands for the 5-act spiral."""
    _configure_spiral(spiral_scale)
    s = sets or {}
    t = timing or Timing()
    cmds: List[Dict] = build_materials(s)
    cmds += build_background()
    cmds += build_odds(t.odds_start,
                       base_sz=s.get('odds', {}).get('size', 0.92))
    cmds += build_naturals(t.nat_start,
                           base_sz=s.get('naturals', {}).get('size', 0.92))
    cmds += build_integers(t.int_start,
                           base_sz=s.get('integers', {}).get('size', 0.80))
    cmds += build_rationals(t.rat_start,
                            base_sz=s.get('rationals', {}).get('size', 0.70))
    cmds += build_irrationals(t.real_start,
                              base_sz=s.get('reals', {}).get('size', 0.70))
    cmds += build_labels(t, label_sz=label_size)
    return cmds
