# File: tests/mocks/meshes_collection.py
# Collection for managing mesh data objects. Mimics bpy.data.meshes with
# creation and management of mesh data for objects like cubes and spheres.
# All Rights Reserved Arodi Emmanuel

from typing import Dict, List, Optional


class MockMesh:
    """Minimal mesh data representation."""

    def __init__(self, name: str):
        self.name: str = name
        self.vertices: List = []
        self.edges: List = []
        self.polygons: List = []

    def __repr__(self) -> str:
        return f"MockMesh(name='{self.name}')"


class MeshesCollection:
    """Collection mimicking bpy.data.meshes."""

    def __init__(self):
        self._meshes: Dict[str, MockMesh] = {}

    def new(self, name: str) -> MockMesh:
        """Create a new mesh with unique name."""
        unique_name = self._make_unique_name(name)
        mesh = MockMesh(unique_name)
        self._meshes[unique_name] = mesh
        return mesh

    def get(self, name: str) -> Optional[MockMesh]:
        """Get mesh by name."""
        return self._meshes.get(name)

    def remove(self, mesh: MockMesh) -> None:
        """Remove mesh from collection."""
        if mesh.name in self._meshes:
            del self._meshes[mesh.name]

    def _make_unique_name(self, name: str) -> str:
        """Ensure unique name."""
        if name not in self._meshes:
            return name
        counter = 1
        while f"{name}.{counter:03d}" in self._meshes:
            counter += 1
        return f"{name}.{counter:03d}"

    def keys(self) -> List[str]:
        return list(self._meshes.keys())

    def __contains__(self, name: str) -> bool:
        return name in self._meshes

    def __getitem__(self, name: str) -> MockMesh:
        return self._meshes[name]

    def __len__(self) -> int:
        return len(self._meshes)
