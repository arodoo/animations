# File: app/commands/rotate_object.py
# Command to rotate an object using euler angles. Supports rotation in
# radians for X, Y, Z axes with optional keyframe insertion.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data


@register_command('rotate_object')
def rotate_object(args: Dict[str, Any]) -> DispatchResult:
    """Rotate an object to specified euler angles."""
    obj_name = args.get('name')
    rotation = args.get('rotation')

    if not obj_name:
        return DispatchResult.fail(
            "Missing 'name' argument",
            command='rotate_object'
        )
    if rotation is None:
        return DispatchResult.fail(
            "Missing 'rotation' argument",
            command='rotate_object'
        )

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Object not found: {obj_name}",
            command='rotate_object'
        )

    obj.rotation_euler = tuple(rotation)

    frame = args.get('frame')
    if frame is not None:
        obj.keyframe_insert('rotation_euler', frame=int(frame))

    return DispatchResult.ok(
        data={'name': obj_name, 'rotation': tuple(rotation)},
        command='rotate_object'
    )
