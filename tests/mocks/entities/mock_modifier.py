# File: tests/mocks/mock_modifier.py
# Modifier entity for mock bpy. Stores modifier type and configurable
# properties dictionary for procedural mesh deformation commands.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict


class MockModifier:
    """Mock Blender Modifier with properties dict."""

    VALID_TYPES = {
        'SUBSURF', 'MIRROR', 'ARRAY', 'BEVEL', 'SOLIDIFY',
        'BOOLEAN', 'ARMATURE', 'CURVE', 'SHRINKWRAP'
    }

    def __init__(self, name: str, mod_type: str):
        self.name: str = name
        self.type: str = mod_type
        self.show_viewport: bool = True
        self.show_render: bool = True
        self._properties: Dict[str, Any] = self._default_props(mod_type)

    def _default_props(self, mod_type: str) -> Dict[str, Any]:
        """Get default properties for modifier type."""
        defaults = {
            'SUBSURF': {'levels': 1, 'render_levels': 2},
            'MIRROR': {'use_axis': (True, False, False)},
            'ARRAY': {'count': 2, 'relative_offset': (1, 0, 0)},
            'BEVEL': {'width': 0.1, 'segments': 1},
        }
        return defaults.get(mod_type, {})

    def __getattr__(self, name: str) -> Any:
        if name.startswith('_'):
            raise AttributeError(name)
        return self._properties.get(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ('name', 'type', 'show_viewport', 'show_render', '_properties'):
            super().__setattr__(name, value)
        else:
            self._properties[name] = value

    def __repr__(self) -> str:
        return f"MockModifier(name='{self.name}', type='{self.type}')"
