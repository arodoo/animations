# File: tests/mocks/bpy_data.py
# Module mimicking bpy.data with collections for objects, meshes, materials.
# Central data repository for the mock Blender environment.
# All Rights Reserved Arodi Emmanuel

from typing import Dict
from ..data.objects_collection import ObjectsCollection
from ..data.meshes_collection import MeshesCollection
from ..data.materials_collection import MaterialsCollection
from ..entities.mock_camera import MockCamera
from ..entities.mock_light import MockLight
from ..data.mock_collection import MockCollection


class MockData:
    """Mock bpy.data module with all collections."""

    def __init__(self):
        self.objects = ObjectsCollection()
        self.meshes = MeshesCollection()
        self.materials = MaterialsCollection()
        self.cameras: Dict[str, MockCamera] = {}
        self.lights: Dict[str, MockLight] = {}
        self.collections: Dict[str, MockCollection] = {}

    def reset(self) -> None:
        """Reset all data to initial state."""
        self.objects = ObjectsCollection()
        self.meshes = MeshesCollection()
        self.materials = MaterialsCollection()
        self.cameras.clear()
        self.lights.clear()
        self.collections.clear()


# Singleton instance
data = MockData()
