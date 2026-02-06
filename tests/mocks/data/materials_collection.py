# File: tests/mocks/materials_collection.py
# Collection for managing materials. Mimics bpy.data.materials with create
# and retrieve functionality for the procedural animation system.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Optional

from ..entities.mock_material import MockMaterial


class MaterialsCollection:
    """Collection mimicking bpy.data.materials."""

    def __init__(self):
        self._materials: Dict[str, MockMaterial] = {}

    def new(self, name: str) -> MockMaterial:
        """Create a new material."""
        unique_name = self._make_unique_name(name)
        mat = MockMaterial(unique_name)
        self._materials[unique_name] = mat
        return mat

    def get(self, name: str) -> Optional[MockMaterial]:
        """Get material by name."""
        return self._materials.get(name)

    def remove(self, mat: MockMaterial) -> None:
        """Remove material."""
        if mat.name in self._materials:
            del self._materials[mat.name]

    def _make_unique_name(self, name: str) -> str:
        if name not in self._materials:
            return name
        counter = 1
        while f"{name}.{counter:03d}" in self._materials:
            counter += 1
        return f"{name}.{counter:03d}"

    def keys(self) -> List[str]:
        return list(self._materials.keys())

    def __contains__(self, name: str) -> bool:
        return name in self._materials

    def __len__(self) -> int:
        return len(self._materials)
