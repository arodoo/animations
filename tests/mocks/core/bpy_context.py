# File: tests/mocks/bpy_context.py
# Module mimicking bpy.context providing access to active scene, object,
# and view layer. Essential for Blender API compatibility.
# All Rights Reserved Arodi Emmanuel

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.mock_object import MockObject


class MockScene:
    """Minimal scene representation."""

    def __init__(self, name: str = "Scene"):
        self.name = name
        self.frame_current: int = 1
        self.frame_start: int = 1
        self.frame_end: int = 250


class MockViewLayer:
    """Minimal view layer for object linking."""

    def __init__(self):
        from ..data.objects_collection import ObjectsCollection
        self.objects = ObjectsCollection()


class MockContext:
    """Mock bpy.context module."""

    def __init__(self):
        self.scene = MockScene()
        self.view_layer = MockViewLayer()
        self.active_object: Optional['MockObject'] = None

    def reset(self) -> None:
        """Reset context to initial state."""
        self.scene = MockScene()
        self.view_layer = MockViewLayer()
        self.active_object = None


# Singleton instance
context = MockContext()
