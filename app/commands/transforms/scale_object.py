# File: app/commands/scale_object.py
# Command to scale an object uniformly or per-axis. Supports scale factors
# for X, Y, Z axes with optional keyframe insertion for animations.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from domain.dispatch_result import DispatchResult
from app.registry import register_command
from infra.bridge import data


@register_command('scale_object')
def scale_object(args: Dict[str, Any]) -> DispatchResult:
    """Scale an object to specified scale factors."""
    obj_name = args.get('name')
    scale = args.get('scale')

    if not obj_name:
        return DispatchResult.fail(
            "Missing 'name' argument",
            command='scale_object'
        )
    if scale is None:
        return DispatchResult.fail(
            "Missing 'scale' argument",
            command='scale_object'
        )

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Object not found: {obj_name}",
            command='scale_object'
        )

    obj.scale = tuple(scale)

    frame = args.get('frame')
    if frame is not None:
        obj.keyframe_insert('scale', frame=int(frame))

    return DispatchResult.ok(
        data={'name': obj_name, 'scale': tuple(scale)},
        command='scale_object'
    )
