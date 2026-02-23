# File: app/commands/spawn_primitive.py
# Command to spawn primitive objects (cube, sphere, plane, etc.) at given
# location. Supports all basic Blender primitives via bpy.ops.mesh calls.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import ops, data, context


PRIMITIVE_MAP = {
    'cube': ops.mesh.primitive_cube_add,
    'sphere': ops.mesh.primitive_uv_sphere_add,
    'plane': ops.mesh.primitive_plane_add,
    'torus': ops.mesh.primitive_torus_add,
    'cone': ops.mesh.primitive_cone_add,
    'cylinder': ops.mesh.primitive_cylinder_add,
}


@register_command('spawn_primitive')
def spawn_primitive(args: Dict[str, Any]) -> DispatchResult:
    """Spawn a primitive object at specified location."""
    primitive_type = args.get('type', 'cube').lower()
    location = tuple(args.get('location', (0, 0, 0)))
    name = args.get('name')

    if primitive_type not in PRIMITIVE_MAP:
        return DispatchResult.fail(
            f"Unknown primitive: {primitive_type}",
            command='spawn_primitive'
        )

    # Forward supported kwargs from the args dict to the primitive operator.
    # We explicitly pop out our control keys and pass the rest through so
    # callers can request segments/subdivisions/major_radius etc.
    op_kwargs = dict(args)
    # Remove keys not accepted by the bpy ops
    for k in ('type', 'name', 'location'):
        op_kwargs.pop(k, None)

    # Record object names before creating so we can identify created objects
    def _object_names():
        try:
            return set(data.objects.keys())
        except Exception:
            try:
                return {o.name for o in data.objects}
            except Exception:
                return set()

    prev_names = _object_names()

    try:
        PRIMITIVE_MAP[primitive_type](location=location, **op_kwargs)
    except TypeError:
        # Fallback: some mock/bridge implementations may not accept extra
        # kwargs — call without extras in that case.
        try:
            PRIMITIVE_MAP[primitive_type](location=location)
        except Exception as e:
            return DispatchResult.fail(str(e), command='spawn_primitive')
    except Exception as e:
        # Any other error from the operator should be reported so callers
        # don't accidentally rename or operate on stale active objects.
        return DispatchResult.fail(str(e), command='spawn_primitive')

    # Determine the created object robustly by name-difference; fallback to context.active_object
    created_obj = None
    try:
        new_names = _object_names()
        created_names = new_names - prev_names
        if created_names:
            # pick one created object (most operators create single object)
            created_name = next(iter(created_names))
            try:
                created_obj = data.objects.get(created_name) if hasattr(data.objects, 'get') else data.objects[created_name]
            except Exception:
                created_obj = None
    except Exception:
        created_obj = None

    if created_obj is None:
        created_obj = getattr(context, 'active_object', None)

    if name and created_obj:
        try:
            created_obj.name = name
            if getattr(created_obj, 'data', None):
                created_obj.data.name = name
        except Exception:
            pass

        # Optional: apply smooth shading if requested
        shade_smooth = args.get('shade_smooth', False)
        if shade_smooth and getattr(created_obj, 'data', None):
            try:
                for poly in created_obj.data.polygons:
                    poly.use_smooth = True
            except Exception:
                pass

        # Optional: add a subdivision surface modifier if requested
        subsurf_levels = args.get('subsurf_levels')
        if subsurf_levels and getattr(created_obj, 'modifiers', None) is not None:
            try:
                created_obj.modifiers.new('Subsurf', type='SUBSURF')
                created_obj.modifiers['Subsurf'].levels = int(subsurf_levels)
            except Exception:
                pass

    return DispatchResult.ok(
        data={'type': primitive_type, 'location': location},
        command='spawn_primitive'
    )
