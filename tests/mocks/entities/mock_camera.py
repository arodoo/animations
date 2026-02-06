# File: tests/mocks/mock_camera.py
# Camera data object for mock bpy. Stores lens focal length, sensor size,
# and depth of field settings for cinematography commands.
# All Rights Reserved Arodi Emmanuel

from typing import Optional


class MockDOFSettings:
    """Depth of field settings for camera."""

    def __init__(self):
        self.use_dof: bool = False
        self.focus_distance: float = 10.0
        self.aperture_fstop: float = 2.8
        self.focus_object: Optional[object] = None


class MockCamera:
    """Mock Blender Camera data."""

    def __init__(self, name: str):
        self.name: str = name
        self.lens: float = 50.0
        self.sensor_width: float = 36.0
        self.dof = MockDOFSettings()
        self.type: str = 'PERSP'

    def __repr__(self) -> str:
        return f"MockCamera(name='{self.name}', lens={self.lens}mm)"
