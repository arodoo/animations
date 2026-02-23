# File moved: scenes/quasar_bh/_physics.py -> animations/_physics.py
# Keplerian physics and accretion disk ring colour/radius data.
# All Rights Reserved Arodi Emmanuel

from math import sqrt

_R_REF = 3.0  # innermost ring radius — normalisation anchor

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

def keplerian_speed(r: float) -> float:
    """Deprecated Newtonian speed. Use pw_angular_velocity instead."""
    return (_R_REF / r) ** 1.5


SCHWARZSCHILD_RADIUS = 1.0  # r_s in scene units; ISCO = 3 r_s


def set_schwarzschild_radius(r_s: float) -> None:
    global SCHWARZSCHILD_RADIUS
    SCHWARZSCHILD_RADIUS = float(r_s)


def isco_radius() -> float:
    return 3.0 * SCHWARZSCHILD_RADIUS


def pw_angular_velocity(r: float) -> float:
    """Paczyński–Wiita angular velocity for a circular orbit at radius r.

    Derived from Φ = -GM/(r - r_s) with GM = 1:

        Ω(r) = sqrt( 1 / ( r · (r - r_s)² ) )

    Captures:
      - ISCO at 3 r_s (matches Schwarzschild GR).
      - Super-Keplerian spin-up as r → r_s.
      - Standard r^(-3/2) falloff for r >> r_s.
    Returns 0 for r ≤ r_s (inside the horizon).
    """
    r_s = SCHWARZSCHILD_RADIUS
    if r <= r_s:
        return 0.0
    return sqrt(1.0 / (r * (r - r_s) ** 2))


def gravitational_redshift_factor(r: float) -> float:
    """sqrt(1 - r_s/r); returns 0 inside the Schwarzschild radius."""
    r_s = SCHWARZSCHILD_RADIUS
    if r <= r_s:
        return 0.0
    return sqrt(max(0.0, 1.0 - (r_s / r)))


def _pw_omega_scaled(r: float) -> float:
    """Alias kept for backwards compatibility."""
    return pw_angular_velocity(r)

