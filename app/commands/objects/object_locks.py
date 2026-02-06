# File: app/commands/object_locks.py
# Lock commands for preventing transform modifications. Essential for
# protecting key objects during complex animation and rigging workflows.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data


@register_command('lock_transforms')
def lock_transforms(args: Dict[str, Any]) -> DispatchResult:
    """Lock object transforms (location, rotation, scale)."""
    obj_name = args.get('name')
    lock_loc = args.get('location', True)
    lock_rot = args.get('rotation', True)
    lock_scale = args.get('scale', True)

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='lock_transforms')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='lock_transforms')

    if lock_loc:
        obj.lock_location = [True, True, True]
    if lock_rot:
        obj.lock_rotation = [True, True, True]
    if lock_scale:
        obj.lock_scale = [True, True, True]

    return DispatchResult.ok({'name': obj_name, 'locked': True}, command='lock_transforms')


@register_command('unlock_transforms')
def unlock_transforms(args: Dict[str, Any]) -> DispatchResult:
    """Unlock object transforms."""
    obj_name = args.get('name')

    if not obj_name:
        return DispatchResult.fail("Missing 'name'", command='unlock_transforms')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(f"Not found: {obj_name}", command='unlock_transforms')

    obj.lock_location = [False, False, False]
    obj.lock_rotation = [False, False, False]
    obj.lock_scale = [False, False, False]

    return DispatchResult.ok({'name': obj_name, 'locked': False}, command='unlock_transforms')
