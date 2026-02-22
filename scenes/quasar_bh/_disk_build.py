# File: scenes/quasar_bh/_disk_build.py
# Disk ring geometry and material creation commands.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List


def ring_emit_strength(i: int) -> float:
    """Emission fades linearly for outer (cooler) rings."""
    return round(8.0 * max(0.3, 1.0 - i * 0.08), 2)


def build_ring(i: int, ring: Dict) -> List[Dict]:
    """Return batch commands for one accretion ring (material + torus)."""
    mat = f"RingMat_{i}"
    r = ring['radius']
    return [
        {'cmd': 'create_material', 'args': {
            'name':          mat,
            'color':         ring['color'] + (1.0,),
            'emit':          True,
            'emit_strength': ring_emit_strength(i),
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'torus', 'name': f"Ring_{i}",
        }},
        {'cmd': 'assign_material', 'args': {
            'object': f"Ring_{i}", 'material': mat,
        }},
        {'cmd': 'scale_object', 'args': {
            'name': f"Ring_{i}", 'scale': (r, r, 0.12),
        }},
    ]
