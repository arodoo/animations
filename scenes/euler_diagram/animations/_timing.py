# File: scenes/euler_diagram/animations/_timing.py
# Timeline for the Expanding Euler Diagram proof.
# All Rights Reserved Arodi Emmanuel

from typing import NamedTuple


class Timing(NamedTuple):
  """Frame offsets for each stage."""
  odds_appear: int = 100
  zoom_start: int = 200
  zoom_end: int = 500
  text_appear: int = 550
