# File: tests/e2e/test_relative_transforms.py
# E2E tests for relative transform commands: translate, rotate, scale
# deltas. Tests incremental movements and accumulation.
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


class TestTranslateRelative:
    def test_translate_adds_delta(self):
        spawn('Cube')
        dispatch_single({
            'cmd': 'translate_relative', 'args': {'name': 'Cube', 'delta': (1, 2, 3)}
        })
        loc = data.objects.get('Cube').location
        assert (loc.x, loc.y, loc.z) == (1, 2, 3)

    def test_translate_accumulates(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'translate_relative', 'args': {'name': 'Cube', 'delta': (1, 0, 0)}},
            {'cmd': 'translate_relative', 'args': {'name': 'Cube', 'delta': (1, 0, 0)}},
        ])
        assert data.objects.get('Cube').location.x == 2


class TestRotateRelative:
    def test_rotate_adds_delta(self):
        spawn('Cube')
        dispatch_single({
            'cmd': 'rotate_relative', 'args': {'name': 'Cube', 'delta': (1.57, 0, 0)}
        })
        rot = data.objects.get('Cube').rotation_euler
        assert abs(rot.x - 1.57) < 0.01


class TestScaleRelative:
    def test_scale_multiplies(self):
        spawn('Cube')
        dispatch_single({
            'cmd': 'scale_relative', 'args': {'name': 'Cube', 'delta': (2, 2, 2)}
        })
        scale = data.objects.get('Cube').scale
        assert (scale.x, scale.y, scale.z) == (2, 2, 2)

    def test_scale_accumulates(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'scale_relative', 'args': {'name': 'Cube', 'delta': (2, 1, 1)}},
            {'cmd': 'scale_relative', 'args': {'name': 'Cube', 'delta': (2, 1, 1)}},
        ])
        assert data.objects.get('Cube').scale.x == 4


class TestTransformUtils:
    def test_reset_transform(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'move_object', 'args': {'name': 'Cube', 'location': (5, 5, 5)}},
            {'cmd': 'reset_transform', 'args': {'name': 'Cube'}},
        ])
        loc = data.objects.get('Cube').location
        assert loc == (0, 0, 0)

    def test_apply_transform(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'move_object', 'args': {'name': 'Cube', 'location': (5, 5, 5)}},
            {'cmd': 'apply_transform', 'args': {'name': 'Cube'}},
        ])
        loc = data.objects.get('Cube').location
        assert loc == (0, 0, 0)
