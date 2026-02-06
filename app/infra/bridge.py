# File: infra/bridge.py
# Bridge module that abstracts bpy import. Tries real Blender bpy first,
# falls back to bpy_mock for testing outside Blender. Single import point.
# All Rights Reserved Arodi Emmanuel

import sys
from typing import TYPE_CHECKING

# Flag to track which implementation is active
_using_mock: bool = False

try:
    import bpy as _bpy
    data = _bpy.data
    context = _bpy.context
    ops = _bpy.ops
except ImportError:
    _using_mock = True
    # Add tests to path for mock import
    from pathlib import Path
    _project_root = Path(__file__).parent.parent
    if str(_project_root) not in sys.path:
        sys.path.insert(0, str(_project_root))

    from tests.mocks.core import bpy_mock as _bpy
    data = _bpy.data
    context = _bpy.context
    ops = _bpy.ops


def is_mock() -> bool:
    """Check if using mock implementation."""
    return _using_mock


def reset() -> None:
    """Reset state (only works with mock)."""
    if _using_mock:
        _bpy.reset_mock()


# Re-export for convenience
bpy = _bpy
