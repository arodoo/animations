# File: tests/mocks/entities/mock_font.py
# Mock FontCurve data for 3D text objects.
# All Rights Reserved Arodi Emmanuel


class MockFontData:
    """Mock bpy.types.TextCurve (FONT object data)."""

    def __init__(self, name: str = "Text"):
        self.name = name
        self.body = ""
        self.extrude = 0.05
        self.align_x = 'CENTER'
        self.align_y = 'CENTER'
