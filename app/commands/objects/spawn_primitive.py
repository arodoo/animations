# File: app/commands/spawn_primitive.py
# Command to spawn primitive objects (cube, sphere, plane, etc.) at given
# location. Supports all basic Blender primitives via bpy.ops.mesh calls.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import ops, data


PRIMITIVE_MAP = {
    'cube': ops.mesh.primitive_cube_add,
    'sphere': ops.mesh.primitive_uv_sphere_add,
    'plane': ops.mesh.primitive_plane_add,
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

    PRIMITIVE_MAP[primitive_type](location=location)

    # Get the created object and rename if needed
    created_objects = list(data.objects.values())
    if created_objects and name:
        obj = created_objects[-1]
        old_name = obj.name
        obj.name = name
        data.objects._objects[name] = data.objects._objects.pop(old_name)

    return DispatchResult.ok(
        data={'type': primitive_type, 'location': location},
        command='spawn_primitive'
    )
