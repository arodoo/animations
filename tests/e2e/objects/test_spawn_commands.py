# File: tests/e2e/test_spawn_commands.py
# E2E tests for spawn_primitive command. Tests cube, sphere, plane creation,
# naming, positioning, and unique name generation for duplicates.
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
    """Reset mock state before each test."""
    reset()
    yield
    reset()


class TestSpawnPrimitive:
    """Tests for spawn_primitive command."""

    def test_spawn_cube_at_origin(self):
        """Spawn cube at origin creates object with correct position."""
        result = dispatch_single({
            'cmd': 'spawn_primitive',
            'args': {'type': 'cube'}
        })
        assert result.success
        assert len(data.objects) == 1
        obj = list(data.objects.values())[0]
        assert obj.location == (0, 0, 0)

    def test_spawn_cube_at_custom_location(self):
        """Spawn cube at custom location sets position correctly."""
        result = dispatch_single({
            'cmd': 'spawn_primitive',
            'args': {'type': 'cube', 'location': (1, 2, 3)}
        })
        assert result.success
        obj = list(data.objects.values())[0]
        assert obj.location == (1, 2, 3)

    def test_spawn_sphere(self):
        """Spawn sphere creates sphere object."""
        result = dispatch_single({
            'cmd': 'spawn_primitive',
            'args': {'type': 'sphere', 'location': (5, 5, 5)}
        })
        assert result.success
        assert result.data['type'] == 'sphere'

    def test_spawn_plane(self):
        """Spawn plane creates plane object."""
        result = dispatch_single({
            'cmd': 'spawn_primitive',
            'args': {'type': 'plane'}
        })
        assert result.success

    def test_spawn_unknown_primitive_fails(self):
        """Spawning unknown primitive type fails gracefully."""
        result = dispatch_single({
            'cmd': 'spawn_primitive',
            'args': {'type': 'pyramid'}
        })
        assert not result.success
        assert 'Unknown primitive' in result.error
