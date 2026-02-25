# File: app/components/bodies/jet_builder.py
# Generic relativistic jet builder: materials, geometry, animation.
# Extracted from scenes/quasar_bh/animations/_bh_jets.py
# and scenes/quasar_bh/animations/_jet_animate.py.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List

from . import jet_physics as jp


_PREC_STEP = 15
_KNOT_STEP = 6


def _jet_materials(cfg: Dict[str, Any]) -> List[Dict]:
    north_emit = round(cfg['base_emission'] * jp.doppler_factor(True), 2)
    south_emit = north_emit
    return [
        {'cmd': 'create_material', 'args': {
            'name': cfg['north_mat'],
            'color': cfg.get('north_color', (0.55, 0.85, 1.0, 1.0)),
            'emit': True, 'emit_strength': north_emit,
        }},
        {'cmd': 'create_material', 'args': {
            'name': cfg['south_mat'],
            'color': cfg.get('south_color', (1.0, 0.40, 0.15, 1.0)),
            'emit': True, 'emit_strength': south_emit,
        }},
    ]


def _jet_geometry(cfg: Dict[str, Any]) -> List[Dict]:
    length = jp.observed_length()
    r_mid  = jp.collimation_radius(length * 0.5)
    parent = cfg['parent_object']
    specs = [
        (cfg['north_name'], length * 0.5,  cfg['north_mat']),
        (cfg['south_name'], -length * 0.5, cfg['south_mat']),
    ]
    cmds: List[Dict] = []
    for name, z_pos, mat in specs:
        cmds += [
            {'cmd': 'spawn_primitive', 'args': {
                'type': 'cylinder', 'name': name,
                'vertices': 32, 'depth': length,
            }},
            {'cmd': 'assign_material', 'args': {
                'object': name, 'material': mat,
            }},
            {'cmd': 'scale_object', 'args': {
                'name': name, 'scale': (r_mid, r_mid, 1.0),
            }},
            {'cmd': 'move_object', 'args': {
                'name': name, 'location': (0, 0, z_pos),
            }},
            {'cmd': 'parent_object', 'args': {
                'child': name, 'parent': parent,
            }},
        ]
    return cmds


def _precession_keys(
    parent: str, total_frames: int,
) -> List[Dict]:
    cmds: List[Dict] = []
    for f in range(1, total_frames + 1, _PREC_STEP):
        t    = (f - 1) / max(total_frames - 1, 1)
        tilt = math.radians(jp.precession_offset(t))
        cmds.append({'cmd': 'rotate_object', 'args': {
            'name': parent, 'rotation': (tilt, 0, 0), 'frame': f,
        }})
    return cmds


def _knot_keys(total_frames: int) -> List[Dict]:
    length = jp.observed_length()
    half   = length * 0.5
    sides  = [('North', -half, +half), ('South', +half, -half)]
    cmds: List[Dict] = []
    for k in range(jp.JET_KNOT_COUNT):
        phase = k / jp.JET_KNOT_COUNT
        for side, z_start, z_end in sides:
            kname = f'Knot{side}_{k}'
            for f in range(1, total_frames + 1, _KNOT_STEP):
                t = ((f - 1) / max(total_frames - 1, 1) + phase) % 1.0
                z = z_start + t * (z_end - z_start)
                s = 1.5 - 0.7 * t
                cmds += [
                    {'cmd': 'move_object', 'args': {
                        'name': kname, 'location': (0, 0, z), 'frame': f,
                    }},
                    {'cmd': 'scale_object', 'args': {
                        'name': kname, 'scale': (s, s, s), 'frame': f,
                    }},
                ]
    return cmds


def _knot_spawn(cfg: Dict[str, Any]) -> List[Dict]:
    cmds: List[Dict] = []
    for k in range(jp.JET_KNOT_COUNT):
        for side in ('North', 'South'):
            kname = f'Knot{side}_{k}'
            mat   = cfg['north_mat'] if side == 'North' else cfg['south_mat']
            jet   = cfg['north_name'] if side == 'North' else cfg['south_name']
            cmds += [
                {'cmd': 'spawn_primitive', 'args': {
                    'type': 'sphere', 'name': kname,
                }},
                {'cmd': 'parent_object', 'args': {
                    'child': kname, 'parent': jet,
                }},
                {'cmd': 'assign_material', 'args': {
                    'object': kname, 'material': mat,
                }},
            ]
    return cmds


def build_jets(cfg: Dict[str, Any]) -> List[Dict]:
    """All jet commands: geometry, knot spawn + animation keyframes.

    Args:
        cfg: dict with keys:
            parent_object  — name of the body the jets attach to
            north_name     — jet north cylinder name
            south_name     — jet south cylinder name
            north_mat      — north material name
            south_mat      — south material name
            north_color    — RGBA tuple (default blue-white)
            south_color    — RGBA tuple (default orange-red)
            base_emission  — float
            total_frames   — int
    """
    parent       = cfg['parent_object']
    total_frames = cfg['total_frames']
    cmds = []
    cmds += _jet_materials(cfg)
    cmds += _jet_geometry(cfg)
    cmds += _knot_spawn(cfg)
    cmds += _precession_keys(parent, total_frames)
    cmds += _knot_keys(total_frames)
    return cmds
