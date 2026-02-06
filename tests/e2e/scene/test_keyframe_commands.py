# File: tests/e2e/test_keyframe_commands.py
# E2E tests for keyframe and animation commands. Tests keyframe insertion,
# retrieval, property validation, and animation data structure.
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


def create_cube(name: str = 'AnimCube'):
    dispatch_single({
        'cmd': 'spawn_primitive',
        'args': {'type': 'cube', 'name': name}
    })


class TestSetKeyframe:
    """Tests for set_keyframe command."""

    def test_set_location_keyframe(self):
        """Insert location keyframe stores value."""
        create_cube('Cube')
        dispatch_single({
            'cmd': 'move_object',
            'args': {'name': 'Cube', 'location': (5, 5, 5)}
        })
        result = dispatch_single({
            'cmd': 'set_keyframe',
            'args': {'name': 'Cube', 'property': 'location', 'frame': 10}
        })
        assert result.success
        obj = data.objects.get('Cube')
        assert obj.animation_data.get_value_at_frame('location', 10)

    def test_set_scale_keyframe(self):
        """Insert scale keyframe stores value."""
        create_cube('Cube')
        dispatch_single({
            'cmd': 'scale_object',
            'args': {'name': 'Cube', 'scale': (3, 3, 3)}
        })
        result = dispatch_single({
            'cmd': 'set_keyframe',
            'args': {'name': 'Cube', 'property': 'scale', 'frame': 20}
        })
        assert result.success
        obj = data.objects.get('Cube')
        val = obj.animation_data.get_value_at_frame('scale', 20)
        assert val == (3, 3, 3)

    def test_invalid_property_fails(self):
        """Invalid property name fails."""
        create_cube('Cube')
        result = dispatch_single({
            'cmd': 'set_keyframe',
            'args': {'name': 'Cube', 'property': 'color', 'frame': 1}
        })
        assert not result.success

    def test_multiple_keyframes_on_same_property(self):
        """Multiple keyframes on same property stored correctly."""
        create_cube('Cube')
        dispatch_batch([
            {'cmd': 'set_keyframe', 'args': {
                'name': 'Cube', 'property': 'location', 'frame': 1
            }},
            {'cmd': 'move_object', 'args': {
                'name': 'Cube', 'location': (10, 10, 10)
            }},
            {'cmd': 'set_keyframe', 'args': {
                'name': 'Cube', 'property': 'location', 'frame': 50
            }},
        ])
        obj = data.objects.get('Cube')
        keyframes = obj.animation_data.get_keyframes('location')
        assert len(keyframes) == 2
        assert 1 in keyframes
        assert 50 in keyframes

    def test_keyframe_with_move_frame_arg(self):
        """Move with frame arg auto-inserts keyframe."""
        create_cube('Cube')
        dispatch_single({
            'cmd': 'move_object',
            'args': {'name': 'Cube', 'location': (7, 7, 7), 'frame': 25}
        })
        obj = data.objects.get('Cube')
        val = obj.animation_data.get_value_at_frame('location', 25)
        assert val == (7, 7, 7)
