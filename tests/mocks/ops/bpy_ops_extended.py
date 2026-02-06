# File: tests/mocks/bpy_ops_extended.py
# Extended operators for cameras, lights, and modifiers. Separated from
# base bpy_ops to maintain file size limits and single responsibility.
# All Rights Reserved Arodi Emmanuel

from typing import Set
from ..core import bpy_data
from ..core import bpy_context
from ..entities.mock_object import MockObject
from ..entities.mock_camera import MockCamera
from ..entities.mock_light import MockLight


class CameraOps:
    """Mock camera operators (bpy.ops.camera equivalent)."""

    @staticmethod
    def add_camera(location: tuple = (0, 0, 0)) -> Set[str]:
        """Add a camera object."""
        cam_data = MockCamera("Camera")
        bpy_data.data.cameras[cam_data.name] = cam_data
        obj = bpy_data.data.objects.new("Camera", cam_data)
        obj.type = "CAMERA"
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}


class LightOps:
    """Mock light operators."""

    @staticmethod
    def add_light(
        light_type: str = 'POINT',
        location: tuple = (0, 0, 0)
    ) -> Set[str]:
        """Add a light object."""
        light_data = MockLight("Light", light_type)
        bpy_data.data.lights[light_data.name] = light_data
        obj = bpy_data.data.objects.new("Light", light_data)
        obj.type = "LIGHT"
        obj.location = location
        bpy_context.context.view_layer.objects.link(obj)
        bpy_context.context.active_object = obj
        return {'FINISHED'}
