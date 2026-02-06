# File: tests/mocks/mock_object.py
# Entity representing a Blender Object with transforms (location, rotation,
# scale), animation data, and parenting support. Core building block.
# All Rights Reserved Arodi Emmanuel

from typing import Optional, TYPE_CHECKING

from ..core.vector3 import Vector3
from ..core.animation_data import AnimationData

if TYPE_CHECKING:
    from .mock_object import MockObject


class MockObject:
    """Mock Blender Object with transforms and animation support."""

    def __init__(self, name: str, obj_type: str = "MESH"):
        self.name: str = name
        self.type: str = obj_type
        self._location = Vector3((0.0, 0.0, 0.0))
        self._rotation_euler = Vector3((0.0, 0.0, 0.0))
        self._scale = Vector3((1.0, 1.0, 1.0))
        self.animation_data: AnimationData = AnimationData()
        self.parent: Optional['MockObject'] = None
        self.data: Optional[object] = None
        self.modifiers: list = []
        self.constraints: list = []
        # Visibility
        self.hide_viewport: bool = False
        self.hide_render: bool = False
        self.hide_select: bool = False
        # Locks
        self.lock_location = [False, False, False]
        self.lock_rotation = [False, False, False]
        self.lock_scale = [False, False, False]
        # Materials and display
        self.material_slots: list = []
        self.color = (1.0, 1.0, 1.0, 1.0)
        self.show_name: bool = False

    @property
    def location(self) -> Vector3:
        return self._location

    @location.setter
    def location(self, value) -> None:
        if isinstance(value, Vector3):
            self._location = value.copy()
        else:
            self._location = Vector3(tuple(value))

    @property
    def rotation_euler(self) -> Vector3:
        return self._rotation_euler

    @rotation_euler.setter
    def rotation_euler(self, value) -> None:
        if isinstance(value, Vector3):
            self._rotation_euler = value.copy()
        else:
            self._rotation_euler = Vector3(tuple(value))

    @property
    def scale(self) -> Vector3:
        return self._scale

    @scale.setter
    def scale(self, value) -> None:
        if isinstance(value, Vector3):
            self._scale = value.copy()
        else:
            self._scale = Vector3(tuple(value))

    def keyframe_insert(self, data_path: str, frame: int = 1) -> None:
        """Insert keyframe for data_path at frame."""
        if data_path == "location":
            value = self._location.to_tuple()
        elif data_path == "rotation_euler":
            value = self._rotation_euler.to_tuple()
        elif data_path == "scale":
            value = self._scale.to_tuple()
        else:
            value = getattr(self, data_path, None)
        self.animation_data.insert_keyframe(data_path, frame, value)

    def __repr__(self) -> str:
        return f"MockObject(name='{self.name}', type='{self.type}')"
