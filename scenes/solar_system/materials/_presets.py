# File: scenes/solar_system/materials/_presets.py
# Quality presets for the Solar System animation scene.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

PLANETS = [
    {'name': 'Mercury', 'radius_au': 2.0,  'size': 0.18,
     'color': (0.60, 0.55, 0.50, 1.0), 'inclination_deg': 7.0, 'period_frames': 360},
    {'name': 'Venus',   'radius_au': 3.2,  'size': 0.28,
     'color': (0.95, 0.85, 0.55, 1.0), 'inclination_deg': 3.4, 'period_frames': 920},
    {'name': 'Earth',   'radius_au': 4.6,  'size': 0.30,
     'color': (0.15, 0.40, 0.80, 1.0), 'inclination_deg': 0.0, 'period_frames': 1500},
    {'name': 'Mars',    'radius_au': 6.2,  'size': 0.22,
     'color': (0.85, 0.30, 0.10, 1.0), 'inclination_deg': 1.8, 'period_frames': 2820},
    {'name': 'Ceres',   'radius_au': 8.0,  'size': 0.10,
     'color': (0.75, 0.70, 0.65, 1.0), 'inclination_deg': 10.6, 'period_frames': 5000},
    {'name': 'Jupiter', 'radius_au': 10.8, 'size': 0.70,
     'color': (0.80, 0.65, 0.45, 1.0), 'inclination_deg': 1.3, 'period_frames': 17760},
    {'name': 'Saturn',  'radius_au': 15.5, 'size': 0.60,
     'color': (0.90, 0.80, 0.55, 1.0), 'inclination_deg': 2.5, 'period_frames': 44160},
    {'name': 'Uranus',  'radius_au': 21.0, 'size': 0.45,
     'color': (0.55, 0.85, 0.90, 1.0), 'inclination_deg': 0.8, 'period_frames': 125640},
    {'name': 'Neptune', 'radius_au': 27.0, 'size': 0.43,
     'color': (0.20, 0.35, 0.90, 1.0), 'inclination_deg': 1.8, 'period_frames': 246000},
    {'name': 'Pluto',   'radius_au': 32.0, 'size': 0.12,
     'color': (0.85, 0.80, 0.75, 1.0), 'inclination_deg': 17.1, 'period_frames': 300000},
    {'name': 'Eris',    'radius_au': 38.0, 'size': 0.11,
     'color': (0.95, 0.95, 0.90, 1.0), 'inclination_deg': 44.0, 'period_frames': 350000},
]

PRESETS: Dict[str, Dict[str, Any]] = {
    'low': {
        'total_frames': 1200,
        'cam_step':     30,
        'dof':          False,
        'planets':      PLANETS[:4],
    },
    'medium': {
        'total_frames': 1200,
        'cam_step':     20,
        'dof':          False,
        'planets':      PLANETS[:6],
    },
    'high': {
        'total_frames': 1200,
        'cam_step':     10,
        'dof':          True,
        'planets':      PLANETS,
    },
    'ultra': {
        'total_frames': 1200,
        'cam_step':     5,
        'dof':          True,
        'planets':      PLANETS,
    },
}
