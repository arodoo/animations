# Command Reference — Transforms

Absolute and relative transform commands. All rotation values are in
**radians** (Blender's native unit for `rotation_euler`).

---

## move_object

Set absolute world position. Pass `frame` to insert a location keyframe.

```python
{'cmd': 'move_object', 'args': {
    'name':     'ObjectName',
    'location': (x, y, z),
    'frame':    1,            # optional
}}
```

---

## rotate_object

Set absolute euler rotation in radians. Pass `frame` to keyframe.

```python
{'cmd': 'rotate_object', 'args': {
    'name':     'ObjectName',
    'rotation': (rx, ry, rz),   # radians, NOT degrees
    'frame':    1,               # optional
}}
```

> **Common mistake:** passing degrees. Blender's `rotation_euler` uses
> radians. Use `math.radians(deg)` to convert.
>
> ```python
> import math
> angle_rad = math.radians(90)   # ✓
> angle_bad = 90                 # ✗ — 90 rad ≈ 14 full rotations
> ```

---

## scale_object

Set absolute scale per axis. Pass `frame` to keyframe.

```python
{'cmd': 'scale_object', 'args': {
    'name':  'ObjectName',
    'scale': (sx, sy, sz),
    'frame': 1,               # optional
}}
```

---

## translate_relative

Move by a delta offset from the current position.

```python
{'cmd': 'translate_relative', 'args': {
    'name':  'ObjectName',
    'delta': (dx, dy, dz),
    'frame': 1,               # optional
}}
```

---

## rotate_relative

Rotate by delta angles (radians) added to current rotation.

```python
{'cmd': 'rotate_relative', 'args': {
    'name':  'ObjectName',
    'delta': (drx, dry, drz),
    'frame': 1,               # optional
}}
```

---

## scale_relative

Multiply current scale by per-axis factors.

```python
{'cmd': 'scale_relative', 'args': {
    'name':   'ObjectName',
    'factor': (fx, fy, fz),
    'frame':  1,              # optional
}}
```

---

## reset_transform

Reset to identity: location `(0,0,0)`, rotation `(0,0,0)`, scale `(1,1,1)`.

```python
{'cmd': 'reset_transform', 'args': {'name': 'ObjectName'}}
```

---

## apply_transform

Bake current transforms into mesh data (clears location/rotation/scale).

```python
{'cmd': 'apply_transform', 'args': {'name': 'ObjectName'}}
```

---

## set_origin

Change the object's origin point.

```python
{'cmd': 'set_origin', 'args': {
    'name': 'ObjectName',
    'type': 'CENTER|CURSOR|GEOMETRY',
}}
```
