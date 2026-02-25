# File: scenes/quasar_bh/animations/_jet_animate.py
# Jet animation: knot spawn, precession keyframes, knot travel.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Dict, List
from . import _jet_physics as jp

_PREC_STEP = 15  # frames between precession keyframes
_KNOT_STEP = 6   # frames between knot travel keyframes


def _precession_keys(total_frames: int) -> List[Dict]:
    """Slow precession: keyframe BlackHole X-rotation each _PREC_STEP."""
    cmds: List[Dict] = []
    for f in range(1, total_frames + 1, _PREC_STEP):
        t = (f - 1) / max(total_frames - 1, 1)
        tilt = math.radians(jp.precession_offset(t))
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': 'BlackHole',
            'rotation': (tilt, 0, 0),
            'frame': f,
        }})
    return cmds


def _knot_keys(total_frames: int) -> List[Dict]:
    """Plasma knot travel: BH pole → jet tip in world space, both jets.

    Cylinder local Z: −half = near cap (BH pole), +half = far cap (tip).
    North knots: local −half→+half  → world   0 → +length (outward ✓)
    South knots: local +half→−half  → world   0 → −length (outward ✓)
    """
    length = jp.observed_length()
    half = length * 0.5
    # sign_start/sign_end define local-space travel direction per side
    sides = [
        ('North', -half, +half),   # local: pole→tip = outward +Z in world
        ('South', +half, -half),   # local: pole→tip = outward −Z in world
    ]
    cmds: List[Dict] = []
    for k in range(jp.JET_KNOT_COUNT):
        phase = k / jp.JET_KNOT_COUNT
        for side, z_start, z_end in sides:
            kname = f'Knot{side}_{k}'
            for f in range(1, total_frames + 1, _KNOT_STEP):
                t = ((f - 1) / max(total_frames - 1, 1) + phase) % 1.0
                z = z_start + t * (z_end - z_start)
                # Scale: 1.5 at ejection (root), shrinks to 0.8 at tip
                s = 1.5 - 0.7 * t
                cmds += [
                    {'cmd': 'move_object', 'args': {
                        'name': kname,
                        'location': (0, 0, z),
                        'frame': f,
                    }},
                    {'cmd': 'scale_object', 'args': {
                        'name': kname,
                        'scale': (s, s, s),
                        'frame': f,
                    }},
                ]

    return cmds


def _knot_spawn() -> List[Dict]:
    """Spawn knot spheres, parent to jet column first, then keyframe."""
    cmds: List[Dict] = []
    for k in range(jp.JET_KNOT_COUNT):
        for side in ('North', 'South'):
            kname = f'Knot{side}_{k}'
            cmds += [
                {'cmd': 'spawn_primitive', 'args': {
                    'type': 'sphere', 'name': kname,
                }},
                {'cmd': 'parent_object', 'args': {
                    'child': kname, 'parent': f'Jet{side}',
                }},
                {'cmd': 'assign_material', 'args': {
                    'object': kname, 'material': f'Jet{side}Mat',
                }},
            ]
    return cmds


def build_jet_animation(total_frames: int) -> List[Dict]:
    """Knot spawn + precession + knot travel keyframes for all jets."""
    return (
        _knot_spawn()
        + _precession_keys(total_frames)
        + _knot_keys(total_frames)
    )
