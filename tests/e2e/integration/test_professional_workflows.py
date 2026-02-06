# File: tests/e2e/test_professional_workflows.py
# E2E tests for complex professional workflows combining multiple commands.
# Tests real-world animation scenarios with cameras, lights, materials.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import pytest
from infra.bridge import data, context, reset
from app.dispatcher import dispatch_batch
import app.commands  # noqa: F401


@pytest.fixture(autouse=True)
def clean_state():
    reset()
    yield
    reset()


class TestProductVisualization:
    """Product visualization scene setup workflow."""

    def test_complete_scene_setup(self):
        results = dispatch_batch([
            # Product
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Product'}},
            {'cmd': 'scale_object', 'args': {'name': 'Product', 'scale': (1, 0.5, 0.3)}},
            # Material
            {'cmd': 'create_material', 'args': {'name': 'ProductMat', 'color': (0.8, 0.2, 0.1, 1)}},
            {'cmd': 'assign_material', 'args': {'object': 'Product', 'material': 'ProductMat'}},
            # Camera
            {'cmd': 'create_camera', 'args': {'name': 'MainCam', 'location': (5, -5, 3)}},
            {'cmd': 'set_focal_length', 'args': {'name': 'MainCam', 'focal_length': 85}},
            # Lighting
            {'cmd': 'create_light', 'args': {'name': 'Key', 'type': 'AREA', 'location': (3, -2, 4)}},
            {'cmd': 'set_light_energy', 'args': {'name': 'Key', 'energy': 1000}},
            {'cmd': 'create_light', 'args': {'name': 'Fill', 'type': 'AREA', 'location': (-2, -3, 2)}},
            {'cmd': 'set_light_energy', 'args': {'name': 'Fill', 'energy': 300}},
        ])
        assert all(r.success for r in results)
        assert len(data.objects) == 4  # Product, Camera, 2 Lights


class TestTurntableAnimation:
    """Turntable animation workflow."""

    def test_turntable_with_keyframes(self):
        results = dispatch_batch([
            {'cmd': 'spawn_primitive', 'args': {'type': 'sphere', 'name': 'Hero'}},
            {'cmd': 'set_frame_range', 'args': {'start': 1, 'end': 120}},
            {'cmd': 'set_current_frame', 'args': {'frame': 1}},
            {'cmd': 'rotate_object', 'args': {'name': 'Hero', 'rotation': (0, 0, 0), 'frame': 1}},
            {'cmd': 'rotate_object', 'args': {'name': 'Hero', 'rotation': (0, 0, 6.28), 'frame': 120}},
        ])
        assert all(r.success for r in results)
        obj = data.objects.get('Hero')
        assert obj.animation_data.has_keyframes('rotation_euler')


class TestModularSetup:
    """Modular scene with collections."""

    def test_organized_scene(self):
        results = dispatch_batch([
            # Create objects
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Cube1'}},
            {'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': 'Cube2'}},
            {'cmd': 'create_camera', 'args': {'name': 'Cam'}},
            {'cmd': 'create_light', 'args': {'name': 'Light'}},
            # Organize
            {'cmd': 'create_collection', 'args': {'name': 'Geometry'}},
            {'cmd': 'create_collection', 'args': {'name': 'Lighting'}},
            {'cmd': 'link_to_collection', 'args': {'object': 'Cube1', 'collection': 'Geometry'}},
            {'cmd': 'link_to_collection', 'args': {'object': 'Cube2', 'collection': 'Geometry'}},
            {'cmd': 'link_to_collection', 'args': {'object': 'Light', 'collection': 'Lighting'}},
        ])
        assert all(r.success for r in results)
        assert len(data.collections['Geometry']) == 2
