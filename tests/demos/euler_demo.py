# File: tests/demos/euler_demo.py
# Expanding Euler Diagram demo.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
  sys.path.insert(0, str(project_root))

from scenes.euler_diagram.scene import create_scene
from scenes.euler_diagram.animations._timing import (
  Timing,
)


def create_euler_animation(
  quality: str = 'low',
) -> dict:
  """
  Creates an Expanding Euler Diagram animation.

  Args:
      quality: 'low' | 'high'
  """
  presets = {
    'low': {
      'total_frames': 600,
      'timing': Timing(
        odds_appear=100,
        zoom_start=200,
        zoom_end=500,
        text_appear=550,
      ),
    },
    'high': {
      'total_frames': 1200,
      'timing': Timing(
        odds_appear=150,
        zoom_start=300,
        zoom_end=900,
        text_appear=1000,
      ),
    },
  }

  if quality not in presets:
    raise ValueError(
      f"quality: {list(presets)}; got '{quality}'"
    )

  p = presets[quality]
  result = create_scene(
    total_frames=p['total_frames'],
    timing=p['timing'],
  )
  return {
    **result,
    'quality': quality,
  }
