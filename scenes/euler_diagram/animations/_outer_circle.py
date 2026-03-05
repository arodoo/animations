# File: scenes/euler_diagram/animations/_outer_circle.py
# Large circle with various number types.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List


def build_outer_circle(zoom_frame: int) -> List[Dict]:
  """Large circle: even, negative, rational, irrational."""
  cmds: List[Dict] = [
    {'cmd': 'spawn_primitive', 'args': {
      'type': 'torus',
      'name': 'AllNumbersRing',
      'location': (0, 0, 0),
      'major_radius': 15.0,
      'minor_radius': 0.15,
    }},
    {'cmd': 'assign_material', 'args': {
      'object': 'AllNumbersRing',
      'material': 'RingBlue',
    }},
  ]

  angles = [-15, -12, -8, -5, 5, 10, 14]
  for i, angle_deg in enumerate(angles):
    angle = math.radians(angle_deg)
    x = 10.0 * math.cos(angle)
    y = 10.0 * math.sin(angle)
    name = f'Num{angle_deg}'
    cmds.append({'cmd': 'spawn_primitive', 'args': {
      'type': 'sphere',
      'name': name,
      'location': (x, y, 0.3),
      'radius': 0.25,
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
      'frame': zoom_frame,
    }})

  return cmds
