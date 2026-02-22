# File moved: scenes/quasar_bh/_disk_build.py -> animations/_disk_build.py
# Disk ring geometry and material creation commands.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List
import math

from ._physics import gravitational_redshift_factor, _pw_omega_scaled


def ring_emit_strength(i: int) -> float:
    """Emission fades linearly for outer (cooler) rings."""
    return round(8.0 * max(0.3, 1.0 - i * 0.08), 2)


def build_ring(i: int, ring: Dict) -> List[Dict]:
    """Return batch commands for one accretion ring (material + torus)."""
    mat = f"RingMat_{i}"
    r = ring['radius']
    # Relativistic corrections: gravitational redshift reduces observed
    # photon energy while orbital motion (Doppler) can boost the approaching
    # side. We compute a conservative scalar modifier to the base emission
    # strength to approximate these effects in a view-independent way.
    base_emit = ring_emit_strength(i)
    g_factor = gravitational_redshift_factor(r)
    omega = _pw_omega_scaled(r)
    # approximate tangential velocity (scene units); c is 1.0 by default
    v = abs(r * omega)
    beta = min(v / 1.0, 0.999)
    # modest Doppler-like boosting factor (view-averaged)
    doppler_boost = 1.0 + 0.5 * beta
    emit_strength = round(base_emit * g_factor * doppler_boost, 3)

    # tighter roughness and normal on inner rings for detail
    rough = max(0.12, 0.5 - 0.05 * i)
    normal = max(0.02, 0.16 - 0.01 * i)

    return [
        {'cmd': 'create_material', 'args': {
            'name':          mat,
            'color':         ring['color'] + (1.0,),
            'emit':          True,
            'emit_strength': emit_strength,
            'use_noise_texture': True,
            'roughness': rough,
            'normal_strength': normal,
        }},
        {'cmd': 'spawn_primitive', 'args': {
            'type': 'torus', 'name': f"Ring_{i}",
            'major_segments': 128,
            'minor_segments': 48,
            'major_radius': r,
            'minor_radius': ring.get('width', 0.12),
        }},
        {'cmd': 'assign_material', 'args': {
            'object': f"Ring_{i}", 'material': mat,
        }},
        # No additional scale: radii provided to spawn_primitive
    ]
