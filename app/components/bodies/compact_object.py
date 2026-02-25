# File: app/components/bodies/compact_object.py
# Generic compact-object builder (black hole, neutron star, etc.).
# Extracted from scenes/quasar_bh/animations/_black_hole.py.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List


def build_compact_object(cfg: Dict[str, Any]) -> List[Dict]:
    """Return commands to spawn a compact spherical body.

    Args:
        cfg: dict with keys:
            name          (str)   — object name
            material_name (str)   — material name
            color         (tuple[float,4]) — RGBA
            r_s           (float) — Schwarzschild / physical radius
            segments      (int)   — sphere longitude segments [64]
            ring_count    (int)   — sphere latitude rings     [32]
            subsurf       (bool)  — apply subdivision [True]
    """
    name     = cfg['name']
    mat_name = cfg['material_name']
    color    = cfg['color']
    r_s      = max(0.05, float(cfg.get('r_s', 1.0)))
    segs     = cfg.get('segments', 64)
    rings    = cfg.get('ring_count', 32)
    subsurf  = cfg.get('subsurf', True)

    return [
        {'cmd': 'create_material', 'args': {
            'name': mat_name, 'color': color,
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'sphere', 'name': name,
            'segments': segs, 'ring_count': rings,
            'shade_smooth': True, 'subsurf_levels': 2 if subsurf else 0,
        }},
        {'cmd': 'assign_material', 'args': {
            'object': name, 'material': mat_name,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': name, 'scale': (r_s, r_s, r_s),
        }},
    ]
