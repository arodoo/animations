# File: app/components/disk_builder.py
# Generic accretion-disk ring builder: material + torus geometry.
# Extracted from scenes/quasar_bh/animations/_disk_build.py.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List
import math

from .disk_physics import (
    gravitational_redshift_factor,
    _pw_omega_scaled,
    SCHWARZSCHILD_RADIUS,
)

_BH_CLEARANCE = 0.05  # minimum gap between inner tube edge and r_s


def _minor_radius(
    i: int, r: float,
    ring_radii: List[float],
) -> float:
    """Tube radius for continuous plasma-cloud appearance."""
    if i + 1 < len(ring_radii):
        half_gap = (ring_radii[i + 1] - r) * 1.15
    else:
        half_gap = (ring_radii[-1] - ring_radii[-2]) * 1.15
    heat_factor = max(0.9, 1.45 - i * 0.05)
    raw = half_gap * heat_factor
    max_allowed = r - (SCHWARZSCHILD_RADIUS + _BH_CLEARANCE)
    return round(min(raw, max_allowed), 3)


def build_ring(
    i: int,
    ring: Dict,
    ring_radii: List[float],
    emit_strength_fn,
) -> List[Dict]:
    """Return batch commands for one accretion ring (material + torus).

    Args:
        i               — ring index (0 = innermost)
        ring            — dict with 'radius' and 'color' keys
        ring_radii      — sorted list of all ring radii (for gap calc)
        emit_strength_fn— callable(i) -> float for base emission
    """
    mat = f"RingMat_{i}"
    r   = ring['radius']
    base_emit  = emit_strength_fn(i)
    g_factor   = gravitational_redshift_factor(r)
    omega      = _pw_omega_scaled(r)
    v          = abs(r * omega)
    beta       = min(v / 1.0, 0.999)
    doppler    = 1.0 + 0.5 * beta
    emit       = round(base_emit * g_factor * doppler, 3)
    rough      = 1.0
    normal     = max(0.8, 1.6 - 0.08 * i)
    minor_r    = _minor_radius(i, r, ring_radii)

    return [
        {'cmd': 'create_material', 'args': {
            'name': mat, 'color': ring['color'] + (1.0,),
            'emit': True, 'emit_strength': emit,
            'use_noise_texture': True,
            'roughness': rough, 'normal_strength': normal,
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'torus', 'name': f"Ring_{i}",
            'major_segments': 192, 'minor_segments': 64,
            'major_radius': r, 'minor_radius': minor_r,
        }},
        {'cmd': 'assign_material', 'args': {
            'object': f"Ring_{i}", 'material': mat,
        }},
    ]
