# File: app/commands/set_keyframe.py
# Command to insert keyframes on object properties. Supports location,
# rotation_euler, and scale with frame specification for animation.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from domain.dispatch_result import DispatchResult
from app.registry import register_command
from infra.bridge import data


VALID_PROPERTIES = {'location', 'rotation_euler', 'scale'}


@register_command('set_keyframe')
def set_keyframe(args: Dict[str, Any]) -> DispatchResult:
    """Insert a keyframe on an object property."""
    obj_name = args.get('name')
    prop = args.get('property', 'location')
    frame = args.get('frame', 1)

    if not obj_name:
        return DispatchResult.fail(
            "Missing 'name' argument",
            command='set_keyframe'
        )

    if prop not in VALID_PROPERTIES:
        return DispatchResult.fail(
            f"Invalid property: {prop}. Valid: {VALID_PROPERTIES}",
            command='set_keyframe'
        )

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Object not found: {obj_name}",
            command='set_keyframe'
        )

    obj.keyframe_insert(prop, frame=int(frame))

    return DispatchResult.ok(
        data={'name': obj_name, 'property': prop, 'frame': frame},
        command='set_keyframe'
    )
