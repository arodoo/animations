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

# The explicit whitelist of Blender API kwargs supported by each primitive type.
# This prevents TypeErrors when we pass our engine's custom decorators (like 'shade_smooth')
SUPPORTED_KWARGS = {
    'cube': {'size', 'calc_uvs', 'enter_editmode', 'align', 'rotation', 'scale'},
    'sphere': {'segments', 'ring_count', 'radius', 'calc_uvs', 'enter_editmode', 'align', 'rotation', 'scale'},
    'plane': {'size', 'calc_uvs', 'enter_editmode', 'align', 'rotation', 'scale'},
    'torus': {'major_segments', 'minor_segments', 'major_segments', 'minor_segments', 'major_radius', 'minor_radius', 'abso_major_rad', 'abso_minor_rad', 'generate_uvs', 'enter_editmode', 'align', 'rotation', 'scale'},
    'cone': {'vertices', 'radius1', 'radius2', 'depth', 'end_fill_type', 'calc_uvs', 'enter_editmode', 'align', 'rotation', 'scale'},
    'cylinder': {'vertices', 'radius', 'depth', 'end_fill_type', 'calc_uvs', 'enter_editmode', 'align', 'rotation', 'scale'}
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
    # We explicitly lookup our whitelist to ensure we never send engine decorators
    # (like 'shade_smooth' or 'name') to the low-level Blender C-API.
    allowed_keys = SUPPORTED_KWARGS.get(primitive_type, set())
    op_kwargs = {k: v for k, v in args.items() if k in allowed_keys}

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
    except Exception as e:
        # Any error from the operator should be reported so callers
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
