# File: scenes/quasar_bh/animations/_jet_physics.py
# Relativistic jet physics: Lorentz beaming, collimation, knot emission.
# All Rights Reserved Arodi Emmanuel

from math import sqrt, sin, pi

from ._physics import SCHWARZSCHILD_RADIUS

JET_LORENTZ_FACTOR: float = 7.0   # Γ — typical AGN quasar jet
JET_REST_LENGTH: float = 55.0     # rest-frame half-length (scene units)
JET_BASE_RADIUS: float = 0.18     # collimation pivot radius
JET_PRECESSION_FRACTION: float = 0.25  # cycles per animation
JET_PRECESSION_DEGREES: float = 3.5   # max tilt half-angle (deg)
JET_KNOT_COUNT: int = 3               # discrete plasma knots per jet
JET_BASE_EMISSION: float = 12.0       # approaching-side base emission


def jet_beta() -> float:
    """v/c: β = sqrt(1 - 1/Γ²)."""
    g = JET_LORENTZ_FACTOR
    return sqrt(max(0.0, 1.0 - 1.0 / (g * g)))


def doppler_factor(approaching: bool) -> float:
    """Relativistic beaming D³ flux scalar (on-axis, α=1).

    D = 1/(Γ·(1∓β)): north≫1 (blue, bright), south≪1 (red, dim).
    """
    g = JET_LORENTZ_FACTOR
    b = jet_beta()
    d = 1.0 / (g * (1.0 - b)) if approaching else 1.0 / (g * (1.0 + b))
    return d ** 3


def observed_length() -> float:
    """Lorentz-contracted visual length: L_obs = L_rest / Γ."""
    return JET_REST_LENGTH / JET_LORENTZ_FACTOR


def collimation_radius(z: float) -> float:
    """MHD parabolic funnel → cylindrical: r(z) from BH centre."""
    r_s = SCHWARZSCHILD_RADIUS
    pivot = 5.0 * r_s
    if z <= 0.0:
        return JET_BASE_RADIUS * 0.1
    if z < pivot:
        return JET_BASE_RADIUS * sqrt(z / pivot)
    return JET_BASE_RADIUS * (1.0 + 0.015 * (z - pivot))


def precession_offset(t: float) -> float:
    """Jet-axis tilt in degrees at normalised time t ∈ [0,1]."""
    return JET_PRECESSION_DEGREES * sin(
        2.0 * pi * t / JET_PRECESSION_FRACTION
    )


def knot_emission(age_frac: float, base: float) -> float:
    """Synchrotron-aging brightness: fast rise, sqrt decay."""
    rise = min(1.0, age_frac / 0.08)
    decay = sqrt(max(0.0, 1.0 - age_frac))
    return round(base * rise * decay, 3)
