# File: tests/mocks/objects_collection.py
# Collection that manages MockObjects with CRUD operations. Mimics Blender's
# bpy.data.objects interface with new(), get(), link(), remove() methods.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, Iterator, List, Optional

from ..entities.mock_object import MockObject


class ObjectsCollection:
    """Collection mimicking bpy.data.objects with object management."""

    def __init__(self):
        self._objects: Dict[str, MockObject] = {}

    def new(self, name: str, data: Optional[object] = None) -> MockObject:
        """Create a new object with unique name."""
        unique_name = self._make_unique_name(name)
        obj = MockObject(unique_name)
        obj.data = data
        self._objects[unique_name] = obj
        return obj

    def get(self, name: str) -> Optional[MockObject]:
        """Get object by name, or None if not found."""
        return self._objects.get(name)

    def remove(self, obj: MockObject) -> None:
        """Remove object from collection."""
        if obj.name in self._objects:
            del self._objects[obj.name]

    def link(self, obj: MockObject) -> None:
        """Link existing object to collection."""
        self._objects[obj.name] = obj

    def unlink(self, obj: MockObject) -> None:
        """Unlink object from collection (alias for remove)."""
        self.remove(obj)

    def _make_unique_name(self, name: str) -> str:
        """Ensure unique name by appending .001, .002, etc."""
        if name not in self._objects:
            return name
        counter = 1
        while f"{name}.{counter:03d}" in self._objects:
            counter += 1
        return f"{name}.{counter:03d}"

    def keys(self) -> List[str]:
        """Get list of all object names."""
        return list(self._objects.keys())

    def values(self) -> List[MockObject]:
        """Get list of all objects."""
        return list(self._objects.values())

    def __contains__(self, name: str) -> bool:
        return name in self._objects

    def __getitem__(self, name: str) -> MockObject:
        return self._objects[name]

    def __iter__(self) -> Iterator[MockObject]:
        return iter(self._objects.values())

    def __len__(self) -> int:
        return len(self._objects)
