# File: tests/mocks/animation_data.py
# Entity for storing keyframe animation data. Tracks property values at
# specific frames, mimicking Blender's animation_data and action system.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, Optional


class AnimationData:
    """Stores keyframes per property per frame like Blender's FCurves."""

    def __init__(self):
        self._keyframes: Dict[str, Dict[int, Any]] = {}

    def insert_keyframe(
        self, property_name: str, frame: int, value: Any
    ) -> None:
        """Insert a keyframe for property at given frame."""
        if property_name not in self._keyframes:
            self._keyframes[property_name] = {}
        self._keyframes[property_name][frame] = value

    def get_keyframes(self, property_name: str) -> Dict[int, Any]:
        """Get all keyframes for a property."""
        return self._keyframes.get(property_name, {}).copy()

    def get_value_at_frame(
        self, property_name: str, frame: int
    ) -> Optional[Any]:
        """Get value at specific frame, or None if not keyed."""
        prop_keys = self._keyframes.get(property_name, {})
        return prop_keys.get(frame)

    def has_keyframes(self, property_name: str) -> bool:
        """Check if property has any keyframes."""
        return property_name in self._keyframes

    def clear_keyframes(self, property_name: Optional[str] = None) -> None:
        """Clear keyframes for property, or all if None."""
        if property_name is None:
            self._keyframes.clear()
        elif property_name in self._keyframes:
            del self._keyframes[property_name]

    def get_all_properties(self) -> list:
        """Get list of all animated property names."""
        return list(self._keyframes.keys())

    def __repr__(self) -> str:
        return f"AnimationData(properties={list(self._keyframes.keys())})"
