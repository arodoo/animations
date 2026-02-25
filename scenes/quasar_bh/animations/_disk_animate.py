# File: scenes/quasar_bh/animations/_disk_animate.py
# Quasar disk-animation wrapper — delegates to app.components.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.disk_animator import build_disk_animation as _build
from ._disk_build import ring_emit_strength


def build_disk_animation(
    disk_rings: List[Dict], total_frames: int,
    rotations: int, step: int,
    pulse_inner: bool, particles: bool,
) -> List[Dict]:
    """Build disk animation using the generic disk_animator."""
    return _build({
        'disk_rings':     disk_rings,
        'total_frames':   total_frames,
        'rotations':      rotations,
        'step':           step,
        'pulse_inner':    pulse_inner,
        'particles':      particles,
        'emit_strength_fn': ring_emit_strength,
    })
