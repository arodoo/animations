# File: app/commands/transforms/apply_transform.py
# Bake object transforms into mesh data.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import data, is_mock


@register_command('apply_scale')
def apply_scale(
    args: Dict[str, Any],
) -> DispatchResult:
    """Bake object scale into mesh, reset to 1.

    After this call the object's scale is (1,1,1)
    and the mesh reflects the original dimensions.
    Children parented afterwards will NOT inherit
    any residual scale.
    """
    obj_name = args.get('name')
    if not obj_name:
        return DispatchResult.fail(
            "Missing 'name'",
            command='apply_scale',
        )
    obj = data.objects.get(obj_name)
    if not obj:
        return DispatchResult.fail(
            f"Not found: {obj_name}",
            command='apply_scale',
        )
    if is_mock():
        return DispatchResult.ok(
            {'name': obj_name},
            command='apply_scale',
        )
    try:
        import mathutils
        s = obj.scale
        obj.data.transform(
            mathutils.Matrix.Diagonal((*s, 1.0))
        )
        obj.scale = (1.0, 1.0, 1.0)
    except Exception as e:
        raise RuntimeError(
            f"apply_scale failed: {e}"
        )
    return DispatchResult.ok(
        {'name': obj_name},
        command='apply_scale',
    )
