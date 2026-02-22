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

    try:
        PRIMITIVE_MAP[primitive_type](location=location, **op_kwargs)
    except TypeError:
        # Fallback: some mock/bridge implementations may not accept extra
        # kwargs — call without extras in that case.
        PRIMITIVE_MAP[primitive_type](location=location)

    # Use the active object (set by the op) to rename — works in both Blender and mock
    if name:
        obj = context.active_object
        if obj:
            obj.name = name
            if obj.data:
                obj.data.name = name

            # Optional: apply smooth shading if requested
            shade_smooth = args.get('shade_smooth', False)
            if shade_smooth and getattr(obj, 'data', None):
                try:
                    for poly in obj.data.polygons:
                        poly.use_smooth = True
                except Exception:
                    # Ignore in mocks or if geometry API is absent
                    pass

            # Optional: add a subdivision surface modifier if requested
            subsurf_levels = args.get('subsurf_levels')
            if subsurf_levels and getattr(obj, 'modifiers', None) is not None:
                try:
                    obj.modifiers.new('Subsurf', type='SUBSURF')
                    obj.modifiers['Subsurf'].levels = int(subsurf_levels)
                except Exception:
                    pass

    return DispatchResult.ok(
        data={'type': primitive_type, 'location': location},
        command='spawn_primitive'
    )
