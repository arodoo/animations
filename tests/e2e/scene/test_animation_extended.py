# File: tests/e2e/test_animation_extended.py
# E2E tests for extended animation commands: delete keyframe, clear
# animation, frame range. Tests advanced keyframe management.
# All Rights Reserved Arodi Emmanuel

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import pytest
from app.infra.bridge import data, context, reset
from app.kernel.dispatcher import dispatch_single, dispatch_batch
import app.commands  # noqa: F401


@pytest.fixture(autouse=True)
def clean_state():
    reset()
    yield
    reset()


def spawn(name: str):
    dispatch_single({'cmd': 'spawn_primitive', 'args': {'type': 'cube', 'name': name}})


class TestDeleteKeyframe:
    def test_delete_specific_keyframe(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'set_keyframe', 'args': {'name': 'Cube', 'frame': 1}},
            {'cmd': 'set_keyframe', 'args': {'name': 'Cube', 'frame': 10}},
            {'cmd': 'delete_keyframe', 'args': {
                'name': 'Cube', 'property': 'location', 'frame': 1
            }},
        ])
        obj = data.objects.get('Cube')
        keyframes = obj.animation_data.get_keyframes('location')
        assert 1 not in keyframes
        assert 10 in keyframes


class TestClearAnimation:
    def test_clear_all_keyframes(self):
        spawn('Cube')
        dispatch_batch([
            {'cmd': 'set_keyframe', 'args': {'name': 'Cube', 'frame': 1}},
            {'cmd': 'set_keyframe', 'args': {'name': 'Cube', 'frame': 10}},
            {'cmd': 'clear_animation', 'args': {'name': 'Cube'}},
        ])
        obj = data.objects.get('Cube')
        assert not obj.animation_data.has_keyframes('location')


class TestFrameOperations:
    def test_set_current_frame(self):
        dispatch_single({'cmd': 'set_current_frame', 'args': {'frame': 50}})
        assert context.scene.frame_current == 50

    def test_set_frame_range(self):
        dispatch_single({
            'cmd': 'set_frame_range', 'args': {'start': 1, 'end': 120}
        })
        assert context.scene.frame_start == 1
        assert context.scene.frame_end == 120
