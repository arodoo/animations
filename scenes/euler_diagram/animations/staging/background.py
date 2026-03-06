# Background plane + reference grid sized for R_MAX=35.54.
# Grid goes to 80 BU, axes to 75 BU depth.

from typing import Dict, List


def build_background() -> List[Dict]:
    return [
        {'cmd': 'create_plane', 'args': {
            'name': 'BackgroundPlane',
            'size': 160.0,
            'location': (0.0, 0.0, -0.5),
            'material': {'color': (0.01, 0.012, 0.03, 1.0),
                         'emission_strength': 0.0},
        }},
        {'cmd': 'create_grid', 'args': {
            'name': 'ReferenceGrid',
            'size': 80.0,
            'grid_scale': 4.0,
            'location': (0.0, 0.0, -0.3),
            'material': {'color': (0.04, 0.05, 0.12, 1.0),
                         'emission_strength': 0.3},
        }},
        {'cmd': 'create_axis', 'args': {
            'name': 'AxisX',
            'axis': 'X',
            'depth': 75.0,
            'radius': 0.06,
            'material': {'color': (0.8, 0.1, 0.1, 1.0),
                         'emission_strength': 2.0},
        }},
        {'cmd': 'create_axis', 'args': {
            'name': 'AxisY',
            'axis': 'Y',
            'depth': 75.0,
            'radius': 0.06,
            'material': {'color': (0.1, 0.8, 0.1, 1.0),
                         'emission_strength': 2.0},
        }},
    ]
