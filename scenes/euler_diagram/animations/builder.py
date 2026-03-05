# Orchestrates all sub-builders for the Euler Diagram.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from .domain.timing import Timing
from .domain.spiral import configure as _cfg_spiral
from .staging.materials import build_materials
from .staging.background import build_background
from .staging.labels import build_labels
from .sets.odds import build_odds
from .sets.naturals import build_naturals
from .sets.integers import build_integers
from .sets.rationals import build_rationals
from .sets.irrationals import build_irrationals


def build_euler_diagram(
    total_frames: int,
    timing: Timing = None,
    spiral_scale: float = 1.0,
    sets: dict = None,
    label_size: float = 1.80,
) -> List[Dict]:
    """Build all commands for the 5-act spiral."""
    _cfg_spiral(spiral_scale)
    s = sets or {}
    t = timing or Timing()
    cmds: List[Dict] = build_materials(s)
    cmds += build_background()
    cmds += build_odds(
        t.odds_start,
        base_sz=s.get('odds', {}).get('size', 1.00),
        total_frames=total_frames,
    )
    cmds += build_naturals(
        t.nat_start,
        base_sz=s.get('naturals', {}).get('size', 0.88),
        total_frames=total_frames,
    )
    cmds += build_integers(
        t.int_start,
        base_sz=s.get('integers', {}).get('size', 0.82),
        total_frames=total_frames,
    )
    cmds += build_rationals(
        t.rat_start,
        base_sz=s.get('rationals', {}).get('size', 0.75),
        total_frames=total_frames,
    )
    cmds += build_irrationals(
        t.real_start,
        base_sz=s.get('reals', {}).get('size', 0.75),
        total_frames=total_frames,
    )
    cmds += build_labels(t, label_sz=label_size)
    return cmds
