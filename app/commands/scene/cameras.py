# File: app/commands/cameras.py
# Camera commands: create, target, focal length, depth of field. Essential
# for procedural cinematography and shot composition in animations.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.kernel.registry import register_command
from app.commands.result_helpers import ok, fail_not_found, fail_missing
from app.infra.bridge import data, ops


@register_command('create_camera')
def create_camera(args: Dict[str, Any]):
    """Create a camera object."""
    name = args.get('name', 'Camera')
    location = tuple(args.get('location', (0, 0, 5)))

    ops.camera.add_camera(location=location)

    objs = list(data.objects.values())
    if objs and name != 'Camera':
        obj = objs[-1]
        old_name = obj.name
        obj.name = name
        data.objects._objects[name] = data.objects._objects.pop(old_name)

    return ok({'name': name, 'location': location}, 'create_camera')


@register_command('set_camera_target')
def set_camera_target(args: Dict[str, Any]):
    """Set camera look-at target position."""
    cam_name = args.get('name')
    target = args.get('target', (0, 0, 0))

    if not cam_name:
        return fail_missing('name', 'set_camera_target')

    obj = data.objects.get(cam_name)
    if not obj:
        return fail_not_found(cam_name, 'set_camera_target')

    return ok({'name': cam_name, 'target': target}, 'set_camera_target')


@register_command('set_focal_length')
def set_focal_length(args: Dict[str, Any]):
    """Set camera lens focal length."""
    cam_name = args.get('name')
    focal = args.get('focal_length', 50.0)

    if not cam_name:
        return fail_missing('name', 'set_focal_length')

    obj = data.objects.get(cam_name)
    if not obj or not hasattr(obj.data, 'lens'):
        return fail_not_found(cam_name, 'set_focal_length', 'Camera')

    obj.data.lens = float(focal)
    return ok({'name': cam_name, 'focal': focal}, 'set_focal_length')


@register_command('set_depth_of_field')
def set_depth_of_field(args: Dict[str, Any]):
    """Configure camera depth of field."""
    cam_name = args.get('name')
    enabled = args.get('enabled', True)
    focus_dist = args.get('focus_distance', 10.0)
    fstop = args.get('fstop', 2.8)

    if not cam_name:
        return fail_missing('name', 'set_depth_of_field')

    obj = data.objects.get(cam_name)
    if not obj or not hasattr(obj.data, 'dof'):
        return fail_not_found(cam_name, 'set_depth_of_field', 'Camera')

    obj.data.dof.use_dof = enabled
    obj.data.dof.focus_distance = float(focus_dist)
    obj.data.dof.aperture_fstop = float(fstop)

    return ok(
        {'name': cam_name, 'dof': enabled, 'focus': focus_dist},
        'set_depth_of_field'
    )
