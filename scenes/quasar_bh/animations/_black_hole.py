# File: scenes/quasar_bh/animations/_black_hole.py
# Quasar black-hole wrapper — delegates to app.components.
# All Rights Reserved Arodi Emmanuel

from typing import List

from app.components.bodies.compact_object import build_compact_object as _build
import app.components.disk_physics as dp


def build_black_hole() -> List[dict]:
    """Build the central black hole using the generic compact builder."""
    return _build({
        'name':          'BlackHole',
        'material_name': 'BlackHoleMat',
        'color':         (0, 0, 0, 1),
        'r_s':           dp.SCHWARZSCHILD_RADIUS,
        'segments':      64,
        'ring_count':    32,
        'subsurf':       True,
    })
