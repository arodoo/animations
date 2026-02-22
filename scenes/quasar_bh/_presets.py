# File: scenes/quasar_bh/_presets.py
# Quality preset definitions for the quasar animation scene.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

PRESETS: Dict[str, Dict[str, Any]] = {
    'low': {
        'total_frames':    900,
        'disk_ring_count': 5,
        'disk_rotations':  8,
        'cam_step':        30,
        'disk_step':       30,
        'eevee_samples':   8,
        'width':           1280,
        'height':          720,
        'particles':       False,
        'pulse_inner':     False,
        'dof':             False,
    },
    'medium': {
        'total_frames':    1800,
        'disk_ring_count': 7,
        'disk_rotations':  12,
        'cam_step':        20,
        'disk_step':       20,
        'eevee_samples':   16,
        'width':           1280,
        'height':          720,
        'particles':       False,
        'pulse_inner':     False,
        'dof':             True,
    },
    'high': {
        'total_frames':    3600,
        'disk_ring_count': 9,
        'disk_rotations':  18,
        'cam_step':        10,
        'disk_step':       10,
        'eevee_samples':   32,
        'width':           1920,
        'height':          1080,
        'particles':       False,
        'pulse_inner':     True,
        'dof':             True,
    },
    'ultra': {
        'total_frames':    3600,
        'disk_ring_count': 9,
        'disk_rotations':  24,
        'cam_step':        5,
        'disk_step':       5,
        'eevee_samples':   64,
        'width':           1920,
        'height':          1080,
        'particles':       True,
        'pulse_inner':     True,
        'dof':             True,
    },
}
