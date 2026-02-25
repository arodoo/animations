# File: app/components/bodies/jet_physics.py
# Generic relativistic jet physics: beaming, collimation, precession.
# Extracted from scenes/quasar_bh/animations/_jet_physics.py.
# All Rights Reserved Arodi Emmanuel

from math import sqrt, sin, pi

from app.components.disk_physics import SCHWARZSCHILD_RADIUS

# Default constants — scenes override by patching their local copy
JET_LORENTZ_FACTOR: float = 7.0
JET_REST_LENGTH: float    = 300.0
JET_BASE_RADIUS: float    = 0.06
JET_PRECESSION_FRACTION: float = 0.25
JET_PRECESSION_DEGREES: float  = 3.5
JET_KNOT_COUNT: int            = 10
JET_BASE_EMISSION: float       = 30.0


def jet_beta() -> float:
    """v/c: β = sqrt(1 - 1/Γ²)."""
    g = JET_LORENTZ_FACTOR
    return sqrt(max(0.0, 1.0 - 1.0 / (g * g)))


def doppler_factor(approaching: bool) -> float:
    """Relativistic beaming D³ flux scalar (on-axis, α=1)."""
    g = JET_LORENTZ_FACTOR
    b = jet_beta()
    d = 1.0 / (g * (1.0 - b)) if approaching else 1.0 / (g * (1.0 + b))
    return d ** 3


def observed_length() -> float:
    """Lorentz-contracted visual length: L_obs = L_rest / Γ."""
    return JET_REST_LENGTH / JET_LORENTZ_FACTOR


def collimation_radius(z: float) -> float:
    """MHD parabolic funnel → recollimated cylinder."""
    r_s = SCHWARZSCHILD_RADIUS
    z0, z1 = 2.0 * r_s, 10.0 * r_s
    if z <= 0.0:
        return JET_BASE_RADIUS * 0.05
    if z < z0:
        return JET_BASE_RADIUS * sqrt(z / z0)
    if z < z1:
        return JET_BASE_RADIUS * (z / z0) ** 0.3
    r_at_z1 = JET_BASE_RADIUS * (z1 / z0) ** 0.3
    return r_at_z1 * (z / z1) ** 0.05


def precession_offset(t: float) -> float:
    """Jet-axis tilt in degrees at normalised time t ∈ [0,1]."""
    return JET_PRECESSION_DEGREES * sin(
        2.0 * pi * t / JET_PRECESSION_FRACTION
    )


def knot_emission(age_frac: float, base: float) -> float:
    """Synchrotron-aging brightness: fast rise, sqrt decay."""
    rise  = min(1.0, age_frac / 0.08)
    decay = sqrt(max(0.0, 1.0 - age_frac))
    return round(base * rise * decay, 3)
