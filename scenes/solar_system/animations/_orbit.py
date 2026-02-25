# File: scenes/solar_system/animations/_orbit.py
# Circular Keplerian planetary orbits using sin/cos keyframes.
# Only new logic for the Solar System — env and camera are parent
# components. Uses app.components.disk_physics.keplerian_speed
# for angular velocity (simple Newtonian, no P-W needed here).
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

from app.components.disk_physics import keplerian_speed


def _planet_ang_velocity(radius_au: float) -> float:
    """Newtonian angular velocity, normalised to inner planet."""
    return keplerian_speed(radius_au)


def _spawn_planet(planet: Dict[str, Any]) -> List[Dict]:
    name = planet['name']
    size = planet['size']
    return [
        {'cmd': 'create_material', 'args': {
            'name':  f"{name}Mat",
            'color': planet['color'],
            'emit':  False,
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'type':         'sphere',
            'name':         name,
            'segments':     32,
            'ring_count':   16,
            'shade_smooth': True,
        }},
        {'cmd': 'assign_material', 'args': {
            'object':   name,
            'material': f"{name}Mat",
        }},
        {'cmd': 'scale_object', 'args': {
            'name':  name,
            'scale': (size, size, size),
        }},
    ]


def _orbit_keys(
    planet: Dict[str, Any], total_frames: int, step: int,
) -> List[Dict]:
    """Circular orbit keyframes using cos/sin on the XY plane."""
    name   = planet['name']
    r      = planet['radius_au']
    period = planet.get('period_frames', total_frames)
    cmds: List[Dict] = []
    for f in range(1, total_frames + 1, step):
        angle = 2.0 * math.pi * (f / period)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        cmds.append({'cmd': 'move_object', 'args': {
            'name':     name,
            'location': (x, y, 0.0),
            'frame':    f,
        }})
        # Self-rotation proportional to orbital speed
        spin = angle * 5.0
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name':     name,
            'rotation': (0.0, 0.0, spin),
            'frame':    f,
        }})
    return cmds


def build_orbits(
    planets: List[Dict[str, Any]],
    total_frames: int,
    step: int = 10,
) -> List[Dict]:
    """Spawn all planets and animate their circular orbits."""
    cmds: List[Dict] = []
    for planet in planets:
        cmds += _spawn_planet(planet)
        cmds += _orbit_keys(planet, total_frames, step)
    return cmds
