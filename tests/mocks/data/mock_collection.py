# File: tests/mocks/mock_collection.py
# Collection entity for organizing objects. Mimics Blender's collection
# system for scene organization and batch operations on object groups.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.mock_object import MockObject


class MockCollection:
    """Mock Blender Collection for object organization."""

    def __init__(self, name: str):
        self.name: str = name
        self._objects: Dict[str, 'MockObject'] = {}
        self.hide_viewport: bool = False
        self.hide_render: bool = False

    def link(self, obj: 'MockObject') -> None:
        """Link object to collection."""
        self._objects[obj.name] = obj

    def unlink(self, obj: 'MockObject') -> None:
        """Unlink object from collection."""
        if obj.name in self._objects:
            del self._objects[obj.name]

    @property
    def objects(self) -> List['MockObject']:
        """Get all objects in collection."""
        return list(self._objects.values())

    def __contains__(self, obj: 'MockObject') -> bool:
        return obj.name in self._objects

    def __len__(self) -> int:
        return len(self._objects)

    def __repr__(self) -> str:
        return f"MockCollection(name='{self.name}', objects={len(self)})"
