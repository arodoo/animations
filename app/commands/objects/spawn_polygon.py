# File: app/commands/objects/spawn_polygon.py
# Spawn a flat polygon mesh from a list of 2D verts.
# All Rights Reserved Arodi Emmanuel

from typing import Any, Dict

from app.domain.dispatch_result import DispatchResult
from app.kernel.registry import register_command
from app.infra.bridge import (
    data, context, is_mock,
)


@register_command('spawn_polygon')
def spawn_polygon(
    args: Dict[str, Any],
) -> DispatchResult:
    """Spawn flat polygon mesh from (x,y) vertex list."""
    name = args.get('name')
    verts = args.get('verts', [])
    location = tuple(args.get('location', (0, 0, 0)))

    if not name:
        return DispatchResult.fail(
            "Missing 'name'",
            command='spawn_polygon',
        )
    if len(verts) < 3:
        return DispatchResult.fail(
            "Requires >= 3 verts",
            command='spawn_polygon',
        )

    if is_mock():
        obj = data.objects.new(name, None)
        obj.location = location
        context.view_layer.objects.link(obj)
        context.active_object = obj
        return DispatchResult.ok(
            {'name': name, 'location': location},
            command='spawn_polygon',
        )

    try:
        import bpy
        import bmesh as _bm
        mesh = bpy.data.meshes.new(name)
        bm = _bm.new()
        bm_verts = [
            bm.verts.new((x, y, 0.0))
            for x, y in verts
        ]
        bm.faces.new(bm_verts)
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        obj.location = location
        return DispatchResult.ok(
            {'name': name, 'location': location},
            command='spawn_polygon',
        )
    except Exception as e:
        raise RuntimeError(
            f'spawn_polygon failed: {e}'
        )
