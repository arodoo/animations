# File: scenes/solar_system/animations/_orrery.py
# The Orrery clockwork mechanism: Sun core, tracks, and metal arms.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

from app.components.bodies.celestial_body import build_celestial_body
from app.components.bodies.dyson_sphere import build_dyson_sphere


def _build_materials() -> List[Dict]:
    return [
        {'cmd': 'create_metal_material', 'args': {
            'name': 'SunCoreMat',
            'color': (0.8, 0.6, 0.2, 1.0),
            'roughness': 0.15,
            'metallic': 1.0,
            'emit_strength': 2.0,  # Glowing core
        }},
        {'cmd': 'create_metal_material', 'args': {
            'name': 'CopperClockworkMat',
            'color': (0.85, 0.45, 0.20, 1.0), # Brighter, more visible copper
            'roughness': 0.25,
            'metallic': 1.0,
            'emit_strength': 0.8, # Subtle luminescence for space visibility
        }},
        {'cmd': 'create_metal_material', 'args': {
            'name': 'GoldMat',
            'color': (1.0, 0.8, 0.1, 1.0),
            'roughness': 0.05,
            'metallic': 1.0,
            'emit_strength': 3.0,
        }},
        {'cmd': 'create_metal_material', 'args': {
            'name': 'SteelMat',
            'color': (0.4, 0.45, 0.5, 1.0),
            'roughness': 0.3,
            'metallic': 0.9,
        }},
    ]


def _build_sun_core() -> List[Dict]:
    # Sun Core - Standardized spherical body
    return build_celestial_body({
        'name': 'SunCore',
        'radius': 0.9,
        'material': 'SunCoreMat',
        'subsurf': 2,
    })


def _build_center(total_frames: int, step: int) -> List[Dict]:
    cmds = _build_sun_core()
    
    # Parametric Architectural Dyson Cage around the Sun
    cmds += build_dyson_sphere({
        'base_radius': 1.15,
        'ring_thickness': 0.008,
        'materials': ['CopperClockworkMat', 'SteelMat'],
        'meridians': 4,
        'parallels': 3,
        'clearance': 0.02, # 20mm clearance radius expansion per group
        'total_frames': total_frames,
        'step': step
    })
    
    return cmds


def _build_planet_mechanism(
    i: int, planet: Dict, total_frames: int, step: int
) -> List[Dict]:
    name = planet['name']
    r = planet['radius_au']
    size = planet['size']
    period = planet.get('period_frames', total_frames)
    inc_deg = planet.get('inclination_deg', 0.0)
    inc = math.radians(inc_deg)
    mat_name = f"{name}MetalMat"
    
    # Stack arms slightly downward on the central shaft
    z_offset = 0.0
    
    cmds: List[Dict] = []
    
    # Planet Material (Metallic version of its color)
    cmds.append({'cmd': 'create_metal_material', 'args': {
        'name': mat_name,
        'color': planet['color'],
        'roughness': 0.2,
        'metallic': 0.9
    }})
    
    # 1. The Track (Static Torus)
    track = f"{name}_Track"
    cmds.append({'cmd': 'spawn_primitive', 'args': {
        'type': 'torus', 'name': track,
        'major_segments': 128, 'minor_segments': 8,
        'major_radius': r, 'minor_radius': 0.015,
        'shade_smooth': True
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': track, 'material': 'CopperClockworkMat'
    }})
    cmds.append({'cmd': 'move_object', 'args': {
        'name': track, 'location': (0.0, 0.0, z_offset), 'frame': 1
    }})
    # Rotate track by its fixed orbital inclination
    cmds.append({'cmd': 'rotate_object', 'args': {
        'name': track, 'rotation': (inc, 0.0, 0.0), 'frame': 1
    }})
    
    # Orbiting Precession for the Track (so it's not a static ring)
    track_precession_period = period * 4.0 # The track rotates much slower than the planet
    for f in range(1, total_frames + 1, step):
        t_angle = 2.0 * math.pi * (f / track_precession_period)
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': track, 'rotation': (inc, 0.0, t_angle), 'frame': f
        }})
    
    # 2. The Arm (Cylinder connecting center to planet)
    arm = f"{name}_Arm"
    cmds.append({'cmd': 'spawn_primitive', 'args': {
        'type': 'cylinder', 'name': arm,
        'vertices': 16, 'depth': 1.0
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': arm, 'material': 'CopperClockworkMat'
    }})
    # Scale: thin cylinder, length r. It spans -r/2 to r/2 on Z.
    cmds.append({'cmd': 'scale_object', 'args': {
        'name': arm, 'scale': (0.02, 0.02, r)
    }})
    
    # 3. The Planet (Standardized Spherical Architecture)
    cmds += build_celestial_body({
        'name': name,
        'radius': size,
        'material': mat_name,
        'subsurf': 1,
    })
    
    # 4. Animation
    for f in range(1, total_frames + 1, step):
        # Calculate angle
        angle = 2.0 * math.pi * (f / period)
        
        # Move planet to 3D point on track (tilted by inc on X axis)
        px = r * math.cos(angle)
        py = r * math.sin(angle) * math.cos(inc)
        pz = r * math.sin(angle) * math.sin(inc)
        cmds.append({'cmd': 'move_object', 'args': {
            'name': name, 'location': (px, py, pz + z_offset), 'frame': f
        }})
        
        # Self-rotation for the planet
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': name, 'rotation': (inc, 0.0, angle * 4.0), 'frame': f
        }})
        
        # Arm transform
        # The arm spans -r/2 to r/2 on Z. We want it pointing from Origin to Planet.
        # So we rotate it to point at (px, py, pz)
        az = math.atan2(py, px)
        el = math.atan2(pz, math.hypot(px, py))
        
        # Center of the arm is halfway between Origin and Planet
        ax = px / 2.0
        ay = py / 2.0
        az_z = pz / 2.0
        
        cmds.append({'cmd': 'move_object', 'args': {
            'name': arm, 'location': (ax, ay, az_z + z_offset), 'frame': f
        }})
        # Default cylinder points strict UP(+Z).
        # We need it pointing at the planet.
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': arm, 'rotation': (0.0, math.pi / 2.0 - el, az), 'frame': f
        }})

    return cmds


def build_orrery(planets: List[Dict], total_frames: int, step: int) -> List[Dict]:
    cmds = _build_materials()
    cmds += _build_center(total_frames, step)
    for i, p in enumerate(planets):
        cmds += _build_planet_mechanism(i, p, total_frames, step)
    return cmds
