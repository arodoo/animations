# File: scenes/missile_storm/animations/staging/lights.py
# Lighting setup for missile storm scene.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_storm_lights() -> List[Dict]:
    """Create sun + fill light for outdoor scene."""
    cmds: List[Dict] = []
    cmds.append({
        'cmd': 'create_light',
        'args': {
            'name': 'Sun',
            'type': 'SUN',
            'location': (100, 50, 200),
        },
    })
    cmds.append({
        'cmd': 'set_light_energy',
        'args': {'name': 'Sun', 'energy': 5.0},
    })
    cmds.append({
        'cmd': 'create_light',
        'args': {
            'name': 'FillLight',
            'type': 'POINT',
            'location': (-50, -80, 100),
        },
    })
    cmds.append({
        'cmd': 'set_light_energy',
        'args': {
            'name': 'FillLight',
            'energy': 2000.0,
        },
    })
    return cmds
