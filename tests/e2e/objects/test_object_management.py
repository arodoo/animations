# File: tests/e2e/test_object_management.py
# E2E tests for object management commands: clone, rename, select, hide,
# show, lock, unlock. Tests CRUD and visibility operations.
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


class TestCloneObject:
    def test_clone_creates_copy(self):
        spawn('Original')
        result = dispatch_single({
            'cmd': 'clone_object', 'args': {'name': 'Original'}
        })
        assert result.success
        assert len(data.objects) == 2

    def test_clone_with_custom_name(self):
        spawn('Src')
        dispatch_single({
            'cmd': 'clone_object', 'args': {'name': 'Src', 'new_name': 'Dst'}
        })
        assert data.objects.get('Dst') is not None


class TestRenameObject:
    def test_rename_changes_name(self):
        spawn('Old')
        dispatch_single({
            'cmd': 'rename_object', 'args': {'name': 'Old', 'new_name': 'New'}
        })
        assert data.objects.get('New') is not None
        assert data.objects.get('Old') is None


class TestSelectObject:
    def test_select_sets_active(self):
        spawn('Target')
        dispatch_single({'cmd': 'select_object', 'args': {'name': 'Target'}})
        assert context.active_object.name == 'Target'


class TestVisibility:
    def test_hide_object(self):
        spawn('Obj')
        dispatch_single({'cmd': 'hide_object', 'args': {'name': 'Obj'}})
        assert data.objects.get('Obj').hide_viewport is True

    def test_show_object(self):
        spawn('Obj')
        dispatch_batch([
            {'cmd': 'hide_object', 'args': {'name': 'Obj'}},
            {'cmd': 'show_object', 'args': {'name': 'Obj'}},
        ])
        assert data.objects.get('Obj').hide_viewport is False


class TestLocks:
    def test_lock_transforms(self):
        spawn('Locked')
        dispatch_single({'cmd': 'lock_transforms', 'args': {'name': 'Locked'}})
        obj = data.objects.get('Locked')
        assert obj.lock_location == [True, True, True]

    def test_unlock_transforms(self):
        spawn('Obj')
        dispatch_batch([
            {'cmd': 'lock_transforms', 'args': {'name': 'Obj'}},
            {'cmd': 'unlock_transforms', 'args': {'name': 'Obj'}},
        ])
        obj = data.objects.get('Obj')
        assert obj.lock_location == [False, False, False]
