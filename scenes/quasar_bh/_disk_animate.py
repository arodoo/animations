# File: scenes/quasar_bh/_disk_animate.py
# Accretion disk animation: Keplerian rotation, emission pulses, particles.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

from ._physics import keplerian_speed
from ._disk_build import ring_emit_strength

_PULSE_CYCLES = 4  # emission hotspot oscillations per animation

def _rotation_keys(
    i: int, ring: Dict, total_frames: int,
    rotations: int, step: int,
) -> List[Dict]:
    speed = keplerian_speed(ring['radius'])
    keys = []
    for f in range(1, total_frames + 1, step):
        angle = (
            (f / total_frames)
            * 2 * math.pi * rotations * speed
        )
        keys.append({'cmd': 'rotate_object', 'args': {
            'name':     f"Ring_{i}",
            'rotation': (0, 0, angle),
            'frame':    f,
        }})
    return keys

def _pulse_keys(
    i: int, total_frames: int, step: int,
) -> List[Dict]:
    base = ring_emit_strength(i)
    keys = []
    for f in range(1, total_frames + 1, step * 3):
        t = (f - 1) / max(total_frames - 1, 1)
        s = base + base * 0.5 * math.sin(
            t * 2 * math.pi * _PULSE_CYCLES
        )
        keys.append({'cmd': 'keyframe_material_emission', 'args': {
            'material': f"RingMat_{i}",
            'strength': round(s, 3),
            'frame':    f,
        }})
    return keys

def _disk_particles(ring_name: str) -> Dict:
    return {'cmd': 'add_particle_system', 'args': {
        'object':         ring_name,
        'name':           'DiskParticles',
        'count':          3000,
        'lifetime':       45,
        'emit_from':      'FACE',
        'normal_factor':  0.1,
        'tangent_factor': 0.8,
        'gravity':        0.0,
        'size':           0.04,
        'render_type':    'HALO',
    }}

def build_disk_animation(
    disk_rings: List[Dict],
    total_frames: int,
    rotations: int,
    step: int,
    pulse_inner: bool,
    use_particles: bool,
) -> List[Dict]:
    """All animation keyframe commands for the accretion disk."""
    batch: List[Dict] = []
    for i, ring in enumerate(disk_rings):
        batch += _rotation_keys(
            i, ring, total_frames, rotations, step
        )
        if pulse_inner and i < 2:
            batch += _pulse_keys(i, total_frames, step)
        if use_particles and i == 0:
            batch.append(_disk_particles(f"Ring_{i}"))
    return batch
