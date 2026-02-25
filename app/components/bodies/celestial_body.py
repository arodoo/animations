# File: app/components/bodies/celestial_body.py
# Generic high-quality celestial body builder providing a standardized interface
# for creating spherical objects like suns, planets, and moons with professional
# geometric settings and subdivision modifiers.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List


def build_celestial_body(cfg: Dict[str, Any]) -> List[Dict]:
    """Return commands to create and configure a high-quality spherical body.

    Args:
        cfg: dict with configuration:
            name (str): The unique blender object name for the sphere.
            radius (float): Uniform radius scale applied to the primitive.
            material (str): Name of the registered material to assign.
            segments (int): Number of longitudinal segments (default 64).
            ring_count (int): Number of latitudinal rings (default 32).
            subsurf (int): Levels of Catmull-Clark subdivision (default 2).
            smooth (bool): Whether to apply smooth shading (default True).
    """
    name = cfg['name']
    radius = float(cfg.get('radius', 1.0))
    mat = cfg['material']
    segs = int(cfg.get('segments', 64))
    rings = int(cfg.get('ring_count', 32))
    sub = int(cfg.get('subsurf', 2))
    smooth = bool(cfg.get('smooth', True))

    return [
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'sphere',
            'name': name,
            'segments': segs,
            'ring_count': rings,
            'shade_smooth': smooth,
            'subsurf_levels': sub,
        }},
        {'cmd': 'assign_material', 'args': {
            'object': name,
            'material': mat,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': name,
            'scale': (radius, radius, radius),
        }},
    ]
