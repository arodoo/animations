# File: app/commands/animation_ext.py
# Extended animation commands: delete keyframe, clear animation, frame ops.
# Advanced keyframe management for complex procedural animation control.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data, context


@register_command('delete_keyframe')
def delete_keyframe(args: Dict[str, Any]) -> DispatchResult:
    """Delete a specific keyframe."""
    obj_name = args.get('name')
    prop = args.get('property', 'location')
    frame = args.get('frame')

    if not obj_name or frame is None:
        return DispatchResult.fail(
            "Missing arguments", command='delete_keyframe')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Not found: {obj_name}", command='delete_keyframe')

    keyframes = obj.animation_data._keyframes.get(prop, {})
    if int(frame) in keyframes:
        del keyframes[int(frame)]

    return DispatchResult.ok(
        {'name': obj_name, 'property': prop, 'frame': frame},
        command='delete_keyframe'
    )


@register_command('clear_animation')
def clear_animation(args: Dict[str, Any]) -> DispatchResult:
    """Clear all keyframes from object."""
    obj_name = args.get('name')
    prop = args.get('property')  # None = clear all

    if not obj_name:
        return DispatchResult.fail(
            "Missing 'name'", command='clear_animation')

    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Not found: {obj_name}", command='clear_animation')

    obj.animation_data.clear_keyframes(prop)
    return DispatchResult.ok(
        {'name': obj_name, 'cleared': prop or 'all'},
        command='clear_animation')


@register_command('set_current_frame')
def set_current_frame(args: Dict[str, Any]) -> DispatchResult:
    """Set timeline current frame."""
    frame = args.get('frame', 1)

    context.scene.frame_current = int(frame)
    return DispatchResult.ok({'frame': frame}, command='set_current_frame')


@register_command('set_frame_range')
def set_frame_range(args: Dict[str, Any]) -> DispatchResult:
    """Set animation frame range."""
    start = args.get('start', 1)
    end = args.get('end', 250)

    context.scene.frame_start = int(start)
    context.scene.frame_end = int(end)

    return DispatchResult.ok({'start': start, 'end': end}, command='set_frame_range')
