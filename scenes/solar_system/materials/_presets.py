# File: scenes/solar_system/materials/_presets.py
# Quality presets for the Solar System animation scene.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

PLANETS = [
    {'name': 'Mercury', 'radius_au': 2.0,  'size': 0.18,
     'color': (0.60, 0.55, 0.50, 1.0), 'period_frames': 360},
    {'name': 'Venus',   'radius_au': 3.2,  'size': 0.28,
     'color': (0.95, 0.85, 0.55, 1.0), 'period_frames': 920},
    {'name': 'Earth',   'radius_au': 4.6,  'size': 0.30,
     'color': (0.15, 0.40, 0.80, 1.0), 'period_frames': 1500},
    {'name': 'Mars',    'radius_au': 6.2,  'size': 0.22,
     'color': (0.85, 0.30, 0.10, 1.0), 'period_frames': 2820},
    {'name': 'Jupiter', 'radius_au': 10.0, 'size': 0.70,
     'color': (0.80, 0.65, 0.45, 1.0), 'period_frames': 17760},
    {'name': 'Saturn',  'radius_au': 14.5, 'size': 0.60,
     'color': (0.90, 0.80, 0.55, 1.0), 'period_frames': 44160},
    {'name': 'Uranus',  'radius_au': 20.0, 'size': 0.45,
     'color': (0.55, 0.85, 0.90, 1.0), 'period_frames': 125640},
    {'name': 'Neptune', 'radius_au': 26.0, 'size': 0.43,
     'color': (0.20, 0.35, 0.90, 1.0), 'period_frames': 246000},
]

PRESETS: Dict[str, Dict[str, Any]] = {
    'low': {
        'total_frames': 3600,
        'cam_step':     30,
        'dof':          False,
        'planets':      PLANETS[:4],
    },
    'medium': {
        'total_frames': 3600,
        'cam_step':     20,
        'dof':          False,
        'planets':      PLANETS[:6],
    },
    'high': {
        'total_frames': 3600,
        'cam_step':     10,
        'dof':          True,
        'planets':      PLANETS,
    },
    'ultra': {
        'total_frames': 3600,
        'cam_step':     5,
        'dof':          True,
        'planets':      PLANETS,
    },
}
