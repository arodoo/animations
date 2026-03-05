# File: scenes/euler_diagram/animations/_inner_circle.py
# Small circle with odd numbers.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List


def build_inner_circle(odds_frame: int) -> List[Dict]:
  """Small circle with odd numbers 1, 3, 5, 7."""
  cmds: List[Dict] = [
    {'cmd': 'spawn_primitive', 'args': {
      'type': 'torus',
      'name': 'OddsRing',
      'location': (0, 0, 0),
      'major_radius': 3.0,
      'minor_radius': 0.1,
    }},
    {'cmd': 'assign_material', 'args': {
      'object': 'OddsRing',
      'material': 'RingPurple',
    }},
  ]

  odds = [1, 3, 5, 7]
  for i, num in enumerate(odds):
    angle = (i / len(odds)) * math.tau
    x = 2.0 * math.cos(angle)
    y = 2.0 * math.sin(angle)
    name = f'Odd{num}'
    cmds.append({'cmd': 'spawn_primitive', 'args': {
      'type': 'sphere',
      'name': name,
      'location': (x, y, 0.3),
      'radius': 0.2,
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
      'object': name,
      'material': 'TextMaterial',
    }})
    cmds.append({'cmd': 'set_keyframe', 'args': {
      'name': name,
      'attribute': 'hide_render',
      'value': True,
      'frame': 1,
    }})
    cmds.append({'cmd': 'set_keyframe', 'args': {
      'name': name,
      'attribute': 'hide_render',
      'value': False,
      'frame': odds_frame,
    }})

  return cmds
