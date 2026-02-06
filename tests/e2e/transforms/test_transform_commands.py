# File: tests/e2e/test_transform_commands.py
# E2E tests for transform commands: move, rotate, scale. Tests position
# updates, euler rotations, scale factors, and error handling.
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


def create_cube(name: str = 'TestCube'):
    """Helper to create a test cube."""
    dispatch_single({
        'cmd': 'spawn_primitive',
        'args': {'type': 'cube', 'name': name}
    })


class TestMoveObject:
    """Tests for move_object command."""

    def test_move_object_updates_location(self):
        """Moving object updates its location."""
        create_cube('Cube')
        result = dispatch_single({
            'cmd': 'move_object',
            'args': {'name': 'Cube', 'location': (10, 20, 30)}
        })
        assert result.success
        assert data.objects.get('Cube').location == (10, 20, 30)

    def test_move_nonexistent_object_fails(self):
        """Moving nonexistent object fails."""
        result = dispatch_single({
            'cmd': 'move_object',
            'args': {'name': 'Ghost', 'location': (1, 1, 1)}
        })
        assert not result.success
        assert 'not found' in result.error


class TestRotateObject:
    """Tests for rotate_object command."""

    def test_rotate_object_updates_euler(self):
        """Rotating object updates euler angles."""
        create_cube('Cube')
        result = dispatch_single({
            'cmd': 'rotate_object',
            'args': {'name': 'Cube', 'rotation': (1.57, 0, 3.14)}
        })
        assert result.success
        rot = data.objects.get('Cube').rotation_euler
        assert abs(rot.x - 1.57) < 0.01


class TestScaleObject:
    """Tests for scale_object command."""

    def test_scale_object_updates_scale(self):
        """Scaling object updates scale factors."""
        create_cube('Cube')
        result = dispatch_single({
            'cmd': 'scale_object',
            'args': {'name': 'Cube', 'scale': (2, 2, 2)}
        })
        assert result.success
        assert data.objects.get('Cube').scale == (2, 2, 2)

    def test_scale_missing_arg_fails(self):
        """Scale without scale argument fails."""
        create_cube('Cube')
        result = dispatch_single({
            'cmd': 'scale_object',
            'args': {'name': 'Cube'}
        })
        assert not result.success
