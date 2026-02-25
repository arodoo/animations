# File: scenes/quasar_bh/animations/_jet_animate.py
# Compatibility shim — jet animation logic now lives in
# app.components.bodies.jet_builder. This file is kept so
# any existing internal cross-imports resolve without error.
# All Rights Reserved Arodi Emmanuel

from app.components.bodies.jet_builder import (  # noqa: F401
    _precession_keys,
    _knot_keys,
    _knot_spawn,
    build_jets as build_jet_animation,
)
