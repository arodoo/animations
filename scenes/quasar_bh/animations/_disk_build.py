# File moved: scenes/quasar_bh/_disk_build.py -> animations/_disk_build.py
# Disk ring geometry and material creation commands.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List
import math

from ._physics import gravitational_redshift_factor, _pw_omega_scaled, SCHWARZSCHILD_RADIUS

_BH_CLEARANCE = 0.05  # minimum gap between inner tube edge and r_s


def ring_emit_strength(i: int) -> float:
    """Emission fades linearly for outer (cooler) rings."""
    return round(8.0 * max(0.3, 1.0 - i * 0.08), 2)


# Must mirror DISK_RINGS radii in _physics.py exactly.
_RING_RADII = [1.20, 1.70, 2.40, 3.40, 4.82, 6.82, 9.66, 13.67, 19.35]


def _minor_radius(i: int, r: float) -> float:
    """Tube radius clamped so the inner torus edge never covers the BH.

    max_allowed = r - (r_s + clearance) ensures the inner surface of the
    tube stays outside the event horizon with a small visible gap.
    """
    if i + 1 < len(_RING_RADII):
        half_gap = (_RING_RADII[i + 1] - r) * 0.80
    else:
        half_gap = (_RING_RADII[-1] - _RING_RADII[-2]) * 0.80
    heat_factor = max(0.7, 1.25 - i * 0.06)
    raw = half_gap * heat_factor
    max_allowed = r - (SCHWARZSCHILD_RADIUS + _BH_CLEARANCE)
    return round(min(raw, max_allowed), 3)


def build_ring(i: int, ring: Dict) -> List[Dict]:
    """Return batch commands for one accretion ring (material + torus)."""
    mat = f"RingMat_{i}"
    r = ring['radius']
    base_emit = ring_emit_strength(i)
    g_factor = gravitational_redshift_factor(r)
    omega = _pw_omega_scaled(r)
    v = abs(r * omega)
    beta = min(v / 1.0, 0.999)
    doppler_boost = 1.0 + 0.5 * beta
    emit_strength = round(base_emit * g_factor * doppler_boost, 3)

    rough = max(0.05, 0.35 - 0.03 * i)
    # strong noise on inner rings makes the surface look turbulent/cloudy
    normal = max(0.15, 0.55 - 0.04 * i)
    minor_r = _minor_radius(i, r)

    return [
        {'cmd': 'create_material', 'args': {
            'name':              mat,
            'color':             ring['color'] + (1.0,),
            'emit':              True,
            'emit_strength':     emit_strength,
            'use_noise_texture': True,
            'roughness':         rough,
            'normal_strength':   normal,
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'type':           'torus',
            'name':           f"Ring_{i}",
            'major_segments': 192,
            'minor_segments': 64,
            'major_radius':   r,
            'minor_radius':   minor_r,
        }},
        {'cmd': 'assign_material', 'args': {
            'object': f"Ring_{i}", 'material': mat,
        }},
    ]
