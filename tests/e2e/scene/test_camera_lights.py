# File: tests/e2e/test_camera_lights.py
# E2E tests for camera and light commands. Tests creation, configuration,
# and property setting for cinematography setup workflows.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import pytest
from app.infra.bridge import data, reset
from app.kernel.dispatcher import dispatch_single, dispatch_batch
import app.commands  # noqa: F401


@pytest.fixture(autouse=True)
def clean_state():
    reset()
    yield
    reset()


class TestCameras:
    def test_create_camera(self):
        result = dispatch_single({
            'cmd': 'create_camera', 'args': {'name': 'MainCam'}
        })
        assert result.success
        assert data.objects.get('MainCam') is not None

    def test_camera_has_data(self):
        dispatch_single({'cmd': 'create_camera', 'args': {'name': 'Cam'}})
        obj = data.objects.get('Cam')
        assert obj.type == 'CAMERA'

    def test_set_focal_length(self):
        dispatch_single({'cmd': 'create_camera', 'args': {'name': 'Cam'}})
        dispatch_single({
            'cmd': 'set_focal_length', 'args': {'name': 'Cam', 'focal_length': 85}
        })
        obj = data.objects.get('Cam')
        assert obj.data.lens == 85

    def test_set_depth_of_field(self):
        dispatch_single({'cmd': 'create_camera', 'args': {'name': 'Cam'}})
        dispatch_single({
            'cmd': 'set_depth_of_field',
            'args': {'name': 'Cam', 'enabled': True, 'focus_distance': 5, 'fstop': 1.4}
        })
        obj = data.objects.get('Cam')
        assert obj.data.dof.use_dof is True
        assert obj.data.dof.focus_distance == 5


class TestLights:
    def test_create_light(self):
        result = dispatch_single({
            'cmd': 'create_light', 'args': {'name': 'Sun', 'type': 'SUN'}
        })
        assert result.success
        assert data.objects.get('Sun') is not None

    def test_set_light_energy(self):
        dispatch_single({'cmd': 'create_light', 'args': {'name': 'Lamp'}})
        dispatch_single({
            'cmd': 'set_light_energy', 'args': {'name': 'Lamp', 'energy': 500}
        })
        obj = data.objects.get('Lamp')
        assert obj.data.energy == 500

    def test_set_light_color(self):
        dispatch_single({'cmd': 'create_light', 'args': {'name': 'Lamp'}})
        dispatch_single({
            'cmd': 'set_light_color', 'args': {'name': 'Lamp', 'color': (1, 0.5, 0)}
        })
        obj = data.objects.get('Lamp')
        assert obj.data.color == (1, 0.5, 0)

    def test_set_light_type(self):
        dispatch_single({'cmd': 'create_light', 'args': {'name': 'Spot'}})
        dispatch_single({
            'cmd': 'set_light_type', 'args': {'name': 'Spot', 'type': 'SPOT'}
        })
        obj = data.objects.get('Spot')
        assert obj.data.type == 'SPOT'
