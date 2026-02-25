# File: scenes/quasar_bh/animations/_cam.py
# Quasar camera wrapper — delegates to app.components.camera_builder.
# All Rights Reserved Arodi Emmanuel

from typing import List

from app.components.camera_builder import build_camera as _build

_CAM_RADIUS    = 240
_FOCAL_LENGTH  = 85.0


def build_camera(
    total_frames: int, cam_step: int, dof: bool,
) -> List[dict]:
    """Build quasar orbit camera using the generic camera_builder."""
    return _build({
        'name':          'SceneCamera',
        'total_frames':  total_frames,
        'cam_step':      cam_step,
        'radius':        _CAM_RADIUS,
        'focal_length':  _FOCAL_LENGTH,
        'dof':           dof,
        'dof_focus_dist': 3.0,
        'dof_fstop':      1.8,
        'el_base_deg':   35.0,
        'el_amp_deg':    25.0,
        'el_freq':        3.0,
        'breathe_amp':   0.25,
        'breathe_freq':   2.5,
    })
