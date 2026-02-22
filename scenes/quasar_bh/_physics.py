# File: scenes/quasar_bh/_physics.py
# Keplerian physics and accretion disk ring colour/radius data.
# All Rights Reserved Arodi Emmanuel

_R_REF = 3.0  # innermost ring radius — normalisation anchor

# Black-body gradient: 10 000 K white-blue → cool dark-red outer edge
DISK_RINGS = [
    {'radius':  3.0, 'color': (1.00, 1.00, 1.00)},
    {'radius':  4.2, 'color': (1.00, 0.97, 0.75)},
    {'radius':  5.5, 'color': (1.00, 0.85, 0.35)},
    {'radius':  7.0, 'color': (1.00, 0.60, 0.10)},
    {'radius':  8.5, 'color': (1.00, 0.35, 0.03)},
    {'radius': 10.0, 'color': (0.80, 0.15, 0.01)},
    {'radius': 11.5, 'color': (0.55, 0.07, 0.01)},
    {'radius': 13.0, 'color': (0.30, 0.03, 0.01)},
    {'radius': 14.5, 'color': (0.15, 0.01, 0.01)},
]


def keplerian_speed(r: float) -> float:
    """ω ∝ r^(-3/2): angular velocity relative to innermost ring."""
    return (_R_REF / r) ** 1.5
