# File: tests/mocks/mock_light.py
# Light data object for mock bpy. Stores energy, color, and light type
# for lighting setup commands in procedural animation scenes.
# All Rights Reserved Arodi Emmanuel

from typing import Tuple


class MockLight:
    """Mock Blender Light data."""

    VALID_TYPES = {'POINT', 'SUN', 'SPOT', 'AREA'}

    def __init__(self, name: str, light_type: str = 'POINT'):
        self.name: str = name
        self.type: str = light_type if light_type in self.VALID_TYPES else 'POINT'
        self.energy: float = 1000.0
        self.color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
        self.shadow_soft_size: float = 0.25

    def __repr__(self) -> str:
        return f"MockLight(name='{self.name}', type='{self.type}')"
