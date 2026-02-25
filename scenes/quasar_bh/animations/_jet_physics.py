# File: scenes/quasar_bh/animations/_jet_physics.py
# Quasar jet physics — re-exports from app.components.bodies.jet_physics
# with quasar-specific constant values locked in.
# All Rights Reserved Arodi Emmanuel

import app.components.bodies.jet_physics as _jp  # noqa: F401

# Quasar-specific overrides applied at import time
_jp.JET_LORENTZ_FACTOR     = 7.0
_jp.JET_REST_LENGTH        = 300.0
_jp.JET_BASE_RADIUS        = 0.06
_jp.JET_PRECESSION_FRACTION = 0.25
_jp.JET_PRECESSION_DEGREES  = 3.5
_jp.JET_KNOT_COUNT         = 10
_jp.JET_BASE_EMISSION      = 30.0

# Re-export everything so existing internal imports keep working
from app.components.bodies.jet_physics import (  # noqa: F401, E402
    JET_LORENTZ_FACTOR,
    JET_REST_LENGTH,
    JET_BASE_RADIUS,
    JET_PRECESSION_FRACTION,
    JET_PRECESSION_DEGREES,
    JET_KNOT_COUNT,
    JET_BASE_EMISSION,
    jet_beta,
    doppler_factor,
    observed_length,
    collimation_radius,
    precession_offset,
    knot_emission,
)
