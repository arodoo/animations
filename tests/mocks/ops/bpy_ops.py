# File: tests/mocks/bpy_ops.py
# Module mimicking bpy.ops with mesh and object operators for creating
# primitives and performing common operations like delete, duplicate.
# All Rights Reserved Arodi Emmanuel

from typing import Set
from ..core import bpy_data
from ..core import bpy_context


class MeshOps:
    """Mock mesh operators (bpy.ops.mesh)."""

    @staticmethod
    def primitive_cube_add(
        size: float = 2.0,
        location: tuple = (0, 0, 0)
    ) -> Set[str]:
        """Add a cube primitive."""
        mesh = bpy_data.data.meshes.new("Cube")
        obj = bpy_data.data.objects.new("Cube", mesh)
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}

    @staticmethod
    def primitive_uv_sphere_add(
        radius: float = 1.0,
        location: tuple = (0, 0, 0)
    ) -> Set[str]:
        """Add a UV sphere primitive."""
        mesh = bpy_data.data.meshes.new("Sphere")
        obj = bpy_data.data.objects.new("Sphere", mesh)
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}

    @staticmethod
    def primitive_plane_add(
        size: float = 2.0,
        location: tuple = (0, 0, 0)
    ) -> Set[str]:
        """Add a plane primitive."""
        mesh = bpy_data.data.meshes.new("Plane")
        obj = bpy_data.data.objects.new("Plane", mesh)
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}


class ObjectOps:
    """Mock object operators (bpy.ops.object)."""

    @staticmethod
    def delete() -> Set[str]:
        """Delete active object."""
        active = bpy_context.context.active_object
        if active:
            bpy_data.data.objects.remove(active)
            bpy_context.context.view_layer.objects.remove(active)
            bpy_context.context.active_object = None
        return {'FINISHED'}

    @staticmethod
    def select_all(action: str = 'SELECT') -> Set[str]:
        """Select/deselect all objects."""
        return {'FINISHED'}


class Ops:
    """Container for operator submodules."""
    mesh = MeshOps()
    object = ObjectOps()

    # Import extended operators
    from .bpy_ops_extended import CameraOps, LightOps
    camera = CameraOps()
    light = LightOps()


ops = Ops()

