# File: app/components/__init__.py
# Parent component layer — generic, scene-agnostic builders that any
# child animation scene can import to assemble its pipeline.
# All Rights Reserved Arodi Emmanuel

from .env_builder import build_environment
from .camera_builder import build_camera
from .disk_physics import (
    pw_angular_velocity,
    gravitational_redshift_factor,
    keplerian_speed,
    SCHWARZSCHILD_RADIUS,
    set_schwarzschild_radius,
    isco_radius,
)
from .disk_builder import build_ring
from .disk_animator import build_disk_animation

__all__ = [
    'build_environment',
    'build_camera',
    'pw_angular_velocity',
    'gravitational_redshift_factor',
    'keplerian_speed',
    'SCHWARZSCHILD_RADIUS',
    'set_schwarzschild_radius',
    'isco_radius',
    'build_ring',
    'build_disk_animation',
]
