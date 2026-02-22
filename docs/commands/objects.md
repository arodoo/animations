# Command Reference — Objects

Commands that create, delete, and manage scene objects.

---

## spawn_primitive

Create a geometric primitive at a given location.

```python
{'cmd': 'spawn_primitive', 'args': {
    'type':     'cube|sphere|plane|torus|cone|cylinder',
    'name':     'ObjectName',
    'location': (x, y, z),   # optional, default (0,0,0)
}}
```

| Type | Blender operator |
|------|-----------------|
| `cube` | `primitive_cube_add` |
| `sphere` | `primitive_uv_sphere_add` |
| `plane` | `primitive_plane_add` |
| `torus` | `primitive_torus_add` |
| `cone` | `primitive_cone_add` |
| `cylinder` | `primitive_cylinder_add` |

> The created object is renamed immediately via `context.active_object`.
> This works identically in Blender and in the mock.

---

## clear_scene

Delete every object in the scene. Use at the start of a script to remove
Blender's default cube, lamp, and camera.

```python
{'cmd': 'clear_scene', 'args': {}}
```

In Blender: calls `bpy.data.objects.remove(obj, do_unlink=True)` for each
object. In mock: clears the internal `_objects` dict directly.

---

## parent_object

Set a parent–child relationship between two objects.

```python
{'cmd': 'parent_object', 'args': {
    'child':  'ChildName',
    'parent': 'ParentName',   # omit to un-parent
}}
```

---

## delete_object

Remove a single object from the scene.

```python
{'cmd': 'delete_object', 'args': {'name': 'ObjectName'}}
```

---

## clone_object

Duplicate an object, copying its transforms.

```python
{'cmd': 'clone_object', 'args': {
    'name':     'SourceObject',
    'new_name': 'CloneName',   # optional
}}
```

---

## rename_object

Change an object's name.

```python
{'cmd': 'rename_object', 'args': {
    'name':     'OldName',
    'new_name': 'NewName',
}}
```

---

## select_object

Set an object as the active selection.

```python
{'cmd': 'select_object', 'args': {'name': 'ObjectName'}}
```

---

## hide_object / show_object

Toggle viewport visibility.

```python
{'cmd': 'hide_object', 'args': {'name': 'ObjectName'}}
{'cmd': 'show_object', 'args': {'name': 'ObjectName'}}
```

---

## set_render_visibility

Toggle whether the object appears in renders.

```python
{'cmd': 'set_render_visibility', 'args': {
    'name':    'ObjectName',
    'visible': True,
}}
```

---

## lock_transforms / unlock_transforms

Prevent or allow transform modifications on an object.

```python
{'cmd': 'lock_transforms',   'args': {'name': 'ObjectName'}}
{'cmd': 'unlock_transforms', 'args': {'name': 'ObjectName'}}
```
