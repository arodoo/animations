# File: scenes/euler_diagram/animations/_builder.py
# Orchestrates the expanding Euler diagram proof.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from ._materials import build_materials
from ._inner_circle import build_inner_circle
from ._outer_circle import build_outer_circle
from ._timing import Timing


def build_euler_diagram(
  total_frames: int,
  timing: Timing = None,
) -> List[Dict]:
  """
  Build Euler diagram proof:
  1. Small circle reveals odd numbers
  2. Massive zoom-out reveals large circle
  3. Large circle contains all number types
  """
  t = timing or Timing()
  cmds: List[Dict] = build_materials()
  cmds += build_inner_circle(t.odds_appear)
  cmds += build_outer_circle(t.zoom_start)
  return cmds
