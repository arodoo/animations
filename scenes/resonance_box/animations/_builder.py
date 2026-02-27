# File: scenes/resonance_box/animations/_builder.py
# The Resonance Box assembly: builds celestial nodes and attaches music box timing.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

from app.components.bodies.celestial_body import build_celestial_body
from app.components.bodies.dyson_sphere import build_dyson_sphere
from ._materials import generate_glass_planet_material
from ._strobe import build_strobe_keyframes


def _build_center(total_frames: int, step: int) -> List[Dict]:
    cmds = build_celestial_body({
        'name': 'SunCore', 'radius': 0.9,
        'material': 'SunCoreMat', 'subsurf': 2,
    })
    cmds += build_dyson_sphere({
        'base_radius': 1.15, 'ring_thickness': 0.008,
        'materials': ['CopperClockworkMat', 'SteelMat'],
        'meridians': 4, 'parallels': 3, 'clearance': 0.02,
        'total_frames': total_frames, 'step': step
    })
    return cmds


def _build_mechanism(i: int, planet: Dict, total: int, step: int) -> List[Dict]:
    name, r, size = planet['name'], planet['radius_au'], planet['size']
    period = planet.get('period_frames', total)
    inc = math.radians(planet.get('inclination_deg', 0.0))
    mat_name = f"{name}GlassMat"
    cmds: List[Dict] = []
    
    # Material
    cmds.append(generate_glass_planet_material(name, planet['color']))

    # Copper Track
    track = f"{name}_Track"
    cmds.append({'cmd': 'spawn_primitive', 'args': {
        'type': 'torus', 'name': track, 'major_segments': 128, 'minor_segments': 8,
        'major_radius': r, 'minor_radius': 0.015, 'shade_smooth': True
    }})
    cmds.append({'cmd': 'assign_material', 'args': {
        'object': track, 'material': 'CopperClockworkMat'
    }})
    cmds.append({'cmd': 'move_object', 'args': {'name': track, 'location': (0, 0, 0), 'frame': 1}})
    cmds.append({'cmd': 'rotate_object', 'args': {'name': track, 'rotation': (inc, 0, 0), 'frame': 1}})
    
    # Precession of the track
    p_period = period * 4.0
    for f in range(1, total + 1, step):
        t_angle = 2.0 * math.pi * (f / p_period)
        cmds.append({'cmd': 'rotate_object', 'args': {'name': track, 'rotation': (inc, 0, t_angle), 'frame': f}})
    
    # Copper Connecting Arm
    arm = f"{name}_Arm"
    cmds.append({'cmd': 'spawn_primitive', 'args': {'type': 'cylinder', 'name': arm, 'vertices': 16, 'depth': 1.0}})
    cmds.append({'cmd': 'assign_material', 'args': {'object': arm, 'material': 'CopperClockworkMat'}})
    cmds.append({'cmd': 'scale_object', 'args': {'name': arm, 'scale': (0.02, 0.02, r)}})
    
    # Planet Body
    cmds += build_celestial_body({'name': name, 'radius': size, 'material': mat_name, 'subsurf': 1})
    
    # Strobe Keyframes
    cmds += build_strobe_keyframes(mat_name, period, total)
    
    # Animation transform
    for f in range(1, total + 1, step):
        angle = 2.0 * math.pi * (f / period)
        px = r * math.cos(angle)
        py = r * math.sin(angle) * math.cos(inc)
        pz = r * math.sin(angle) * math.sin(inc)
        
        cmds.append({'cmd': 'move_object', 'args': {'name': name, 'location': (px, py, pz), 'frame': f}})
        cmds.append({'cmd': 'rotate_object', 'args': {'name': name, 'rotation': (inc, 0, angle * 4.0), 'frame': f}})
        
        ax, ay, az_z = px / 2.0, py / 2.0, pz / 2.0
        cmds.append({'cmd': 'move_object', 'args': {'name': arm, 'location': (ax, ay, az_z), 'frame': f}})
        
        az = math.atan2(py, px)
        el = math.atan2(pz, math.hypot(px, py))
        cmds.append({'cmd': 'rotate_object', 'args': {'name': arm, 'rotation': (0.0, math.pi / 2.0 - el, az), 'frame': f}})

    return cmds


def build_resonance_box(planets: List[Dict], total_frames: int, step: int) -> List[Dict]:
    """Compile the Resonance Box architecture into a dispatcher payload payload."""
    from ._materials import generate_resonance_materials
    
    cmds = generate_resonance_materials()
    cmds += _build_center(total_frames, step)
    for i, p in enumerate(planets):
        cmds += _build_mechanism(i, p, total_frames, step)
    return cmds
