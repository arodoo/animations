# File: tests/e2e/test_materials.py
# E2E tests for material commands: create, assign, set color. Tests
# material workflow from creation to object assignment.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import pytest
from infra.bridge import data, reset
from app.dispatcher import dispatch_single, dispatch_batch
import app.commands  # noqa: F401


@pytest.fixture(autouse=True)
def clean_state():
    reset()
    yield
    reset()


def spawn(name: str):
    dispatch_single({'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': name}})


class TestMaterials:
    def test_create_material(self):
        result = dispatch_single({
            'cmd': 'create_material', 'args': {'name': 'Red'}
        })
        assert result.success
        assert 'Red' in data.materials.keys()

    def test_create_material_with_color(self):
        dispatch_single({
            'cmd': 'create_material',
            'args': {'name': 'Blue', 'color': (0, 0, 1, 1)}
        })
        mat = data.materials.get('Blue')
        assert mat.diffuse_color[2] == 1.0

    def test_assign_material(self):
        spawn('Cube')
        dispatch_single({'cmd': 'create_material', 'args': {'name': 'Mat'}})
        result = dispatch_single({
            'cmd': 'assign_material',
            'args': {'object': 'Cube', 'material': 'Mat'}
        })
        assert result.success
        assert len(data.objects.get('Cube').material_slots) == 1

    def test_set_material_color(self):
        dispatch_single({'cmd': 'create_material', 'args': {'name': 'Mat'}})
        dispatch_single({
            'cmd': 'set_material_color',
            'args': {'name': 'Mat', 'color': (1, 0, 0, 1)}
        })
        mat = data.materials.get('Mat')
        assert mat.diffuse_color[0] == 1.0

    def test_set_object_color(self):
        spawn('Cube')
        dispatch_single({
            'cmd': 'set_object_color',
            'args': {'name': 'Cube', 'color': (0.5, 0.5, 0.5, 1)}
        })
        obj = data.objects.get('Cube')
        assert obj.color[0] == 0.5
