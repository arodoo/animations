# File: app/commands/advanced/rigid_body.py
# Add rigid body physics to objects.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import (
    data, context, ops, is_mock,
)


@register_command('add_rigid_body')
def add_rigid_body(
    args: Dict[str, Any],
) -> DispatchResult:
    """Add rigid body to an object.

    Args:
        object:      Target object name
        type:        'ACTIVE' | 'PASSIVE'
        mass:        float (default 1.0)
        friction:    float (default 0.5)
        restitution: float (default 0.0)
        kinematic:   bool  (default False)
        collision:   'CONVEX_HULL'|'MESH'|'BOX'
    """
    obj_name = args.get('object')
    if not obj_name:
        return DispatchResult.fail(
            "Missing 'object'",
            command='add_rigid_body',
        )
    if is_mock():
        return DispatchResult.ok(
            {'object': obj_name},
            command='add_rigid_body',
        )
    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Not found: {obj_name}",
            command='add_rigid_body',
        )
    context.view_layer.objects.active = obj
    rb_type = args.get('type', 'ACTIVE')
    ops.rigidbody.object_add(type=rb_type)
    rb = obj.rigid_body
    rb.mass = float(args.get('mass', 1.0))
    rb.friction = float(
        args.get('friction', 0.5),
    )
    rb.restitution = float(
        args.get('restitution', 0.0),
    )
    rb.kinematic = bool(
        args.get('kinematic', False),
    )
    shape = args.get(
        'collision', 'CONVEX_HULL',
    )
    rb.collision_shape = shape
    return DispatchResult.ok(
        {
            'object': obj_name,
            'type': rb_type,
        },
        command='add_rigid_body',
    )
