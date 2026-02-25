# File: app/components/disk_physics.py
# Generic disk/orbital physics: Keplerian, Paczyński-Wiita, redshift.
# Extracted from scenes/quasar_bh/animations/_physics.py.
# All Rights Reserved Arodi Emmanuel

from math import sqrt

_R_REF = 3.0  # innermost ring radius — normalisation anchor

SCHWARZSCHILD_RADIUS: float = 1.0  # r_s in scene units; ISCO = 3 r_s


def set_schwarzschild_radius(r_s: float) -> None:
    global SCHWARZSCHILD_RADIUS
    SCHWARZSCHILD_RADIUS = float(r_s)


def isco_radius() -> float:
    """Innermost stable circular orbit = 3 r_s."""
    return 3.0 * SCHWARZSCHILD_RADIUS


def keplerian_speed(r: float) -> float:
    """Simple Newtonian normalised speed. Use pw_angular_velocity for GR."""
    return (_R_REF / r) ** 1.5


def pw_angular_velocity(r: float) -> float:
    """Paczyński-Wiita angular velocity for a circular orbit at radius r.

    Ω(r) = sqrt( 1 / ( r · (r - r_s)² ) )
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
