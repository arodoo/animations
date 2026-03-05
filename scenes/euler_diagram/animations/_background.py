# File: scenes/euler_diagram/animations/_background.py
# Scalable Cartesian Grid with parallax effect.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_scalable_grid(
  total_frames: int,
) -> List[Dict]:
  """Animated Cartesian grid with parallax-like scaling."""
  cmds: List[Dict] = []

  # Close/far grid planes for parallax
  cmds.append({'cmd': 'create_cartesian_grid', 'args': {
    'size': 200,
    'grid_scale': 10,
    'z_offset': -50.0,
    'bg_color': (0.02, 0.02, 0.025, 1.0),
    'line_color': (0.08, 0.1, 0.15, 1.0),
  }})

  cmds.append({'cmd': 'create_cartesian_grid', 'args': {
    'size': 500,
    'grid_scale': 40,
    'z_offset': -200.0,
    'bg_color': (0.01, 0.01, 0.015, 1.0),
    'line_color': (0.04, 0.05, 0.08, 1.0),
  }})

  return cmds
