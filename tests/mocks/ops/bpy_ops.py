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

    @staticmethod
    def primitive_torus_add(
        location: tuple = (0, 0, 0),
        **kwargs
    ) -> Set[str]:
        """Add a torus primitive."""
        mesh = bpy_data.data.meshes.new("Torus")
        obj = bpy_data.data.objects.new("Torus", mesh)
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}

    @staticmethod
    def primitive_cone_add(
        location: tuple = (0, 0, 0),
        **kwargs
    ) -> Set[str]:
        """Add a cone primitive."""
        mesh = bpy_data.data.meshes.new("Cone")
        obj = bpy_data.data.objects.new("Cone", mesh)
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}

    @staticmethod
    def primitive_cylinder_add(
        location: tuple = (0, 0, 0),
        **kwargs
    ) -> Set[str]:
        """Add a cylinder primitive."""
        mesh = bpy_data.data.meshes.new("Cylinder")
        obj = bpy_data.data.objects.new("Cylinder", mesh)
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}


class ObjectOps:
    """Mock object operators (bpy.ops.object)."""

    @staticmethod
    def light_add(type: str = 'POINT', location: tuple = (0, 0, 0), **kwargs) -> Set[str]:
        """Add a light object (mirrors bpy.ops.object.light_add)."""
        from ..entities.mock_light import MockLight
        light_data = MockLight("Light", type)
        bpy_data.data.lights[light_data.name] = light_data
        obj = bpy_data.data.objects.new("Light", light_data)
        obj.type = "LIGHT"
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}

    @staticmethod
    def camera_add(location: tuple = (0, 0, 0), **kwargs) -> Set[str]:
        """Add a camera (mirrors bpy.ops.object.camera_add)."""
        from ..entities.mock_camera import MockCamera
        cam_data = MockCamera("Camera")
        bpy_data.data.cameras[cam_data.name] = cam_data
        obj = bpy_data.data.objects.new("Camera", cam_data)
        obj.type = "CAMERA"
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}

    @staticmethod
    def empty_add(location: tuple = (0, 0, 0), **kwargs) -> Set[str]:
        """Add an empty object."""
        obj = bpy_data.data.objects.new("Empty", None)
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}

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

