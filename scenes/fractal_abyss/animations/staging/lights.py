# Light configuration for Fractal Abyss.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_lights() -> List[Dict]:
    """Three-point lighting for deep space."""
    return [
        {'cmd': 'set_light_energy', 'args': {
            'name': 'Key', 'energy': 3000.0,
        }},
        {'cmd': 'move_object', 'args': {
            'name': 'Key',
            'location': (0, 0, 50),
        }},
        {'cmd': 'set_light_energy', 'args': {
            'name': 'Fill', 'energy': 1200.0,
        }},
        {'cmd': 'move_object', 'args': {
            'name': 'Fill',
            'location': (25, -20, 40),
        }},
        {'cmd': 'set_light_energy', 'args': {
            'name': 'Rim', 'energy': 800.0,
        }},
        {'cmd': 'move_object', 'args': {
            'name': 'Rim',
            'location': (-15, 25, 35),
        }},
    ]
