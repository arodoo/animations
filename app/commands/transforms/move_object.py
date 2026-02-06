# File: app/commands/move_object.py
# Command to move an object to specified coordinates. Supports absolute
# positioning via location tuple and optional keyframe insertion.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data


@register_command('move_object')
def move_object(args: Dict[str, Any]) -> DispatchResult:
    """Move an object to specified location."""
    obj_name = args.get('name')
    location = args.get('location')

    if not obj_name:
        return DispatchResult.fail(
            "Missing 'name' argument",
            command='move_object'
        )
    if location is None:
        return DispatchResult.fail(
            "Missing 'location' argument",
            command='move_object'
        )

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Object not found: {obj_name}",
            command='move_object'
        )

    obj.location = tuple(location)

    # Optional: insert keyframe
    frame = args.get('frame')
    if frame is not None:
        obj.keyframe_insert('location', frame=int(frame))

    return DispatchResult.ok(
        data={'name': obj_name, 'location': tuple(location)},
        command='move_object'
    )
