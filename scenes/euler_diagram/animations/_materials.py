# File: scenes/euler_diagram/animations/_materials.py
# Material setup for rings and text.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_materials() -> List[Dict]:
  """Create ring materials: purple for odds, blue."""
  cmds: List[Dict] = [
    {'cmd': 'create_material', 'args': {
      'name': 'RingPurple',
      'color': (0.8, 0.2, 0.9, 1.0),
      'emit': True,
      'emit_strength': 5.0,
    }},
    {'cmd': 'create_material', 'args': {
      'name': 'RingBlue',
      'color': (0.2, 0.6, 0.95, 1.0),
      'emit': True,
      'emit_strength': 5.0,
    }},
    {'cmd': 'create_material', 'args': {
      'name': 'TextMaterial',
      'color': (1.0, 1.0, 1.0, 1.0),
      'emit': True,
      'emit_strength': 3.0,
    }},
  ]
  return cmds
