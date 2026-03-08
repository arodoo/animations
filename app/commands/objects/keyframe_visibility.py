# File: app/commands/objects/keyframe_visibility.py
# Keyframed visibility: hide objects at specific frame.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict, List

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data


def _keyframe_hide(obj: Any, frame: int) -> None:
    """Keyframe visibility OFF at frame."""
    obj.hide_viewport = False
    obj.keyframe_insert(
        'hide_viewport', frame=frame - 1,
    )
    obj.hide_viewport = True
    obj.keyframe_insert(
        'hide_viewport', frame=frame,
    )


@register_command('hide_at_frame')
def hide_at_frame(
    args: Dict[str, Any],
) -> DispatchResult:
    """Hide single object at a given frame."""
    name = args.get('name')
    frame = args.get('frame')
    if not name or frame is None:
        return DispatchResult.fail(
            "Missing 'name' or 'frame'",
            command='hide_at_frame',
        )
    obj = data.objects.get(name)
    if not obj:
        return DispatchResult.fail(
            f"Not found: {name}",
            command='hide_at_frame',
        )
    _keyframe_hide(obj, int(frame))
    return DispatchResult.ok(
        {'name': name, 'frame': frame},
        command='hide_at_frame',
    )


@register_command('hide_objects_at_frame')
def hide_objects_at_frame(
    args: Dict[str, Any],
) -> DispatchResult:
    """Hide multiple objects at a given frame."""
    names: List[str] = args.get('names', [])
    frame = args.get('frame')
    if not names or frame is None:
        return DispatchResult.fail(
            "Missing 'names' or 'frame'",
            command='hide_objects_at_frame',
        )
    f = int(frame)
    hidden = []
    for name in names:
        obj = data.objects.get(name)
        if obj:
            _keyframe_hide(obj, f)
            hidden.append(name)
    return DispatchResult.ok(
        {'hidden': hidden, 'frame': f},
        command='hide_objects_at_frame',
    )
