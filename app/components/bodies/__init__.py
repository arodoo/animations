# File: app/components/bodies/__init__.py
# Physical-body builders: compact objects and relativistic jets.
# All Rights Reserved Arodi Emmanuel

from .compact_object import build_compact_object
from .jet_physics import (
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
from .jet_builder import build_jets

__all__ = [
    'build_compact_object',
    'JET_LORENTZ_FACTOR',
    'JET_REST_LENGTH',
    'JET_BASE_RADIUS',
    'JET_PRECESSION_FRACTION',
    'JET_PRECESSION_DEGREES',
    'JET_KNOT_COUNT',
    'JET_BASE_EMISSION',
    'jet_beta',
    'doppler_factor',
    'observed_length',
    'collimation_radius',
    'precession_offset',
    'knot_emission',
    'build_jets',
]
