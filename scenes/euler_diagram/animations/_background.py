# File: scenes/euler_diagram/animations/_background.py
# Scalable Cartesian Grid — parallax via two depths.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def build_scalable_grid(
    zoom_start: int,
    zoom_end: int,
) -> List[Dict]:
    """Two-depth grid: parallax from camera movement."""
    return [
        {'cmd': 'create_cartesian_grid', 'args': {
            'size': 150,
            'grid_scale': 5,
            'z_offset': -12.0,
            'bg_color': (0.01, 0.01, 0.018, 1.0),
            'line_color': (0.05, 0.07, 0.13, 1.0),
        }},
        {'cmd': 'create_cartesian_grid', 'args': {
            'size': 500,
            'grid_scale': 50,
            'z_offset': -80.0,
            'bg_color': (0.004, 0.005, 0.009, 1.0),
            'line_color': (0.02, 0.03, 0.06, 1.0),
        }},
    ]
