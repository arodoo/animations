# File: app/components/camera_builder.py
# Generic spherical-orbit camera builder with optional depth of field.
# Extracted from scenes/quasar_bh/animations/_cam.py.
# All Rights Reserved Arodi Emmanuel

import math
from typing import Any, Dict, List


def build_camera(cfg: Dict[str, Any]) -> List[Dict]:
    """Return commands to create and animate the scene camera.

    Args:
        cfg: dict with keys:
            name             (str)   — object name, e.g. 'SceneCamera'
            total_frames     (int)
            cam_step         (int)   — keyframe interval
            radius           (float) — orbit base radius
            focal_length     (float) — mm
            dof              (bool)  — depth-of-field enabled
            dof_focus_dist   (float) — focus distance (if dof=True)
            dof_fstop        (float) — f-stop (if dof=True)
            el_base_deg      (float) — base elevation degrees [35]
            el_amp_deg       (float) — elevation amplitude     [25]
            el_freq          (float) — elevation freq mult     [3]
            breathe_amp      (float) — radial breathe fraction [0.25]
            breathe_freq     (float) — breathe cycles          [2.5]
    """
    name   = cfg['name']
    r      = cfg['radius']
    frames = cfg['total_frames']
    step   = cfg['cam_step']
    fl     = cfg.get('focal_length', 85.0)
    el_b   = cfg.get('el_base_deg', 35.0)
    el_a   = cfg.get('el_amp_deg', 25.0)
    el_f   = cfg.get('el_freq', 3.0)
    b_amp  = cfg.get('breathe_amp', 0.25)
    b_freq = cfg.get('breathe_freq', 2.5)

    cmds: List[Dict] = [
        {'cmd': 'create_camera',    'args': {'name': name}},
        {'cmd': 'set_focal_length', 'args': {'name': name, 'focal_length': fl}},
    ]
    for f in range(1, frames + 1, step):
        t  = (f - 1) / max(frames - 1, 1)
        az = t * 2 * math.pi
        el = math.radians(el_b + el_a * math.sin(t * el_f * math.pi))
        breathe = b_amp * math.sin(t * b_freq * 2 * math.pi)
        dodge   = math.exp(-((t - 0.5) / 0.08) ** 2)
        r_local = r * (1.0 - breathe - 0.15 * dodge)
        x = r_local * math.cos(el) * math.cos(az)
        y = r_local * math.cos(el) * math.sin(az)
        z = r_local * math.sin(el)
        cmds.append({'cmd': 'move_object', 'args': {
            'name': name, 'location': (x, y, z), 'frame': f,
        }})
    cmds.append({'cmd': 'set_camera_target', 'args': {
        'name': name, 'target': (0, 0, 0),
    }})
    if cfg.get('dof', False):
        cmds.append({'cmd': 'set_depth_of_field', 'args': {
            'name':           name,
            'enabled':        True,
            'focus_distance': cfg.get('dof_focus_dist', 3.0),
            'fstop':          cfg.get('dof_fstop', 1.8),
        }})
    return cmds
