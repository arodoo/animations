# File: scenes/quasar_bh/animations/_physics.py
# Quasar physics — disk ring data + re-exports from app.components.
# All Rights Reserved Arodi Emmanuel

from app.components.disk_physics import (      # noqa: F401 (re-export)
    SCHWARZSCHILD_RADIUS,
    set_schwarzschild_radius,
    isco_radius,
    keplerian_speed,
    pw_angular_velocity,
    gravitational_redshift_factor,
    _pw_omega_scaled,
)

# ── Quasar-specific ring data (not generic) ────────────────────────
DISK_RINGS = [
    {'radius':  1.20, 'color': (1.00, 1.00, 1.00)},
    {'radius':  1.70, 'color': (1.00, 0.97, 0.85)},
    {'radius':  2.40, 'color': (1.00, 0.90, 0.55)},
    {'radius':  3.40, 'color': (1.00, 0.72, 0.20)},
    {'radius':  4.82, 'color': (1.00, 0.48, 0.06)},
    {'radius':  6.82, 'color': (0.90, 0.25, 0.02)},
    {'radius':  9.66, 'color': (0.65, 0.10, 0.01)},
    {'radius': 13.67, 'color': (0.38, 0.04, 0.01)},
    {'radius': 19.35, 'color': (0.18, 0.01, 0.01)},
]
