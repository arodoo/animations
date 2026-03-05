# File: scenes/euler_diagram/animations/_camera.py
# Camera setup with progressive zoom out.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List


def build_camera(
  total_frames: int,
  zoom_start: int,
  zoom_end: int,
) -> List[Dict]:
  """Camera with controlled zoom-out effect."""
  cmds: List[Dict] = [
    {'cmd': 'create_camera', 'args': {
      'name': 'SceneCamera',
    }},
    {'cmd': 'set_focal_length', 'args': {
      'name': 'SceneCamera',
      'focal_length': 50.0,
    }},
    {'cmd': 'set_camera_target', 'args': {
      'name': 'SceneCamera',
      'target': (0, 0, 0),
    }},
    {'cmd': 'set_depth_of_field', 'args': {
      'name': 'SceneCamera',
      'enabled': True,
      'focus_distance': 30.0,
      'fstop': 2.8,
    }},
  ]

  for f in range(1, total_frames + 1, 50):
    if f <= zoom_start:
      dist = 20.0
    elif f >= zoom_end:
      dist = 80.0
    else:
      progress = (f - zoom_start) / (zoom_end - zoom_start)
      dist = 20.0 + (60.0 * progress)

    a = math.radians(45)
    cx = math.cos(a) * dist
    cy = math.sin(a) * dist
    cmds.append({'cmd': 'move_object', 'args': {
      'name': 'SceneCamera',
      'location': (cx, cy, 20.0),
      'frame': f,
    }})

  return cmds
