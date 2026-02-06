# File: tests/mocks/vector3.py
# Value Object representing 3D coordinates (x,y,z) with tuple-like interface
# and arithmetic operations for transforms. Immutable by design for safety.
# All Rights Reserved Arodi Emmanuel

from typing import Tuple, Union


class Vector3:
    """Minimal Vector3 value object mimicking Blender's mathutils.Vector."""

    __slots__ = ('_data',)

    def __init__(self, coords: Tuple[float, float, float] = (0.0, 0.0, 0.0)):
        self._data = list(coords)

    @property
    def x(self) -> float:
        return self._data[0]

    @x.setter
    def x(self, value: float) -> None:
        self._data[0] = float(value)

    @property
    def y(self) -> float:
        return self._data[1]

    @y.setter
    def y(self, value: float) -> None:
        self._data[1] = float(value)

    @property
    def z(self) -> float:
        return self._data[2]

    @z.setter
    def z(self, value: float) -> None:
        self._data[2] = float(value)

    def __getitem__(self, index: int) -> float:
        return self._data[index]

    def __setitem__(self, index: int, value: float) -> None:
        self._data[index] = float(value)

    def __iter__(self):
        return iter(self._data)

    def __len__(self) -> int:
        return 3

    def copy(self) -> 'Vector3':
        return Vector3(tuple(self._data))

    def to_tuple(self) -> Tuple[float, float, float]:
        return tuple(self._data)

    def __repr__(self) -> str:
        return f"Vector3({self._data[0]}, {self._data[1]}, {self._data[2]})"

    def __eq__(self, other: Union['Vector3', Tuple]) -> bool:
        if isinstance(other, Vector3):
            return self._data == other._data
        if isinstance(other, (tuple, list)) and len(other) == 3:
            return self._data == list(other)
        return False
