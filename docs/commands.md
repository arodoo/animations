# Command Reference

Complete reference for all 44 animation engine commands.

---

## Primitives

### spawn_primitive
Create geometric primitive.

```python
{'cmd': 'spawn_primitive', 'args': {
    'type': 'cube|sphere|plane',
    'name': 'ObjectName',
    'location': (x, y, z)  # optional
}}
```

---

## Transform Commands

### move_object
Set absolute position with optional keyframe.

```python
{'cmd': 'move_object', 'args': {
    'name': 'ObjectName',
    'location': (x, y, z),
    'frame': 1  # optional
}}
```

### rotate_object
Set absolute rotation (radians).

```python
{'cmd': 'rotate_object', 'args': {
    'name': 'ObjectName',
    'rotation': (rx, ry, rz),
    'frame': 1  # optional
}}
```

### scale_object
Set absolute scale.

```python
{'cmd': 'scale_object', 'args': {
    'name': 'ObjectName',
    'scale': (sx, sy, sz),
    'frame': 1  # optional
}}
```

---

## Relative Transforms

### translate_relative
Move by delta offset.

```python
{'cmd': 'translate_relative', 'args': {
    'name': 'ObjectName',
    'delta': (dx, dy, dz),
    'frame': 1  # optional
}}
```

### rotate_relative
Rotate by delta angles.

### scale_relative
Scale by delta factors (multiplies).

---

## Transform Utilities

### reset_transform
Reset to identity (0,0,0) location, rotation, (1,1,1) scale.

### apply_transform
Bake transforms to mesh data.

### set_origin
Change object origin point.

```python
{'cmd': 'set_origin', 'args': {
    'name': 'ObjectName',
    'type': 'CENTER|CURSOR|GEOMETRY'
}}
```

---

## Animation

### set_keyframe
Insert keyframe at frame.

### delete_keyframe
Remove specific keyframe.

```python
{'cmd': 'delete_keyframe', 'args': {
    'name': 'ObjectName',
    'property': 'location|rotation_euler|scale',
    'frame': 10
}}
```

### clear_animation
Remove all keyframes.

### set_current_frame
Set timeline position.

### set_frame_range
Set animation start/end frames.

---

## Hierarchy

### parent_object
Set parent-child relationship.

### delete_object
Remove object from scene.

---

## Object Management

### clone_object
Duplicate object.

### rename_object
Change object name.

### select_object
Set as active selection.

---

## Visibility

### hide_object / show_object
Toggle viewport visibility.

### set_render_visibility
Toggle render visibility.

### set_object_color
Set viewport display color (RGBA).

---

## Locks

### lock_transforms / unlock_transforms
Prevent/allow transform modifications.

---

## Materials

### create_material
Create named material with color.

### assign_material
Assign material to object.

### set_material_color
Change material base color.

---

## Cameras

### create_camera
Create camera at location.

### set_camera_target
Set look-at position.

### set_focal_length
Set lens focal length (mm).

### set_depth_of_field
Configure DOF settings.

---

## Lights

### create_light
Create light of type POINT|SUN|SPOT|AREA.

### set_light_energy
Set intensity (watts).

### set_light_color
Set RGB color.

### set_light_type
Change light type.

---

## Modifiers

### add_modifier
Add modifier to object.

```python
{'cmd': 'add_modifier', 'args': {
    'object': 'CubeName',
    'type': 'SUBSURF|MIRROR|ARRAY|BEVEL',
    'name': 'ModifierName'
}}
```

### remove_modifier
Remove modifier by name.

### configure_modifier
Set modifier property value.

---

## Collections

### create_collection
Create named collection.

### link_to_collection
Add object to collection.

### unlink_from_collection
Remove object from collection.
