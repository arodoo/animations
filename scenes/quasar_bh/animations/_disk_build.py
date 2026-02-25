# File: scenes/quasar_bh/animations/_disk_build.py
# Quasar disk-ring wrapper — delegates to app.components.disk_builder.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List

from app.components.disk_builder import build_ring as _build_ring
from ._physics import DISK_RINGS

_RING_RADII = [r['radius'] for r in DISK_RINGS]


def ring_emit_strength(i: int) -> float:
    """Quasar-specific emission: fades for outer (cooler) rings."""
    return round(8.0 * max(0.3, 1.0 - i * 0.08), 2)


def build_ring(i: int, ring: Dict) -> List[Dict]:
    """Build one accretion ring using the generic disk builder."""
    return _build_ring(i, ring, _RING_RADII, ring_emit_strength)
