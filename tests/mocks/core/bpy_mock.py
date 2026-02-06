# File: tests/mocks/bpy_mock.py
# Entry point for the bpy mock module. Exposes data, context, and ops modules
# just like real Blender Python API. Use via infra/bridge.py for abstraction.
# All Rights Reserved Arodi Emmanuel

from .bpy_data import data
from .bpy_context import context
from ..ops.bpy_ops import ops
from .vector3 import Vector3
from ..entities.mock_object import MockObject


def reset_mock() -> None:
    """Reset all mock state for clean test runs."""
    data.reset()
    context.reset()


__all__ = ['data', 'context', 'ops', 'Vector3', 'MockObject', 'reset_mock']
