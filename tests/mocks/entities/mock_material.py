# File: tests/mocks/mock_material.py
# Material entity for mock bpy. Stores color, name, and basic properties
# needed for material assignment workflows in procedural animations.
# All Rights Reserved Arodi Emmanuel

from typing import Tuple


class MockMaterial:
    """Mock Blender Material with basic color properties."""

    def __init__(self, name: str):
        self.name: str = name
        self.diffuse_color: Tuple[float, ...] = (0.8, 0.8, 0.8, 1.0)
        self.use_nodes: bool = False

    def __repr__(self) -> str:
        return f"MockMaterial(name='{self.name}')"
