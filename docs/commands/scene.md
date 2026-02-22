# Command Reference — Scene

Materials, cameras, lights, world environment, and render settings.

---

## Materials

### create_material

Create a named material. In Blender (non-mock), sets up a node-based shader
so colours are visible in Material Preview and Rendered modes.

```python
{'cmd': 'create_material', 'args': {
    'name':          'MaterialName',
    'color':         (r, g, b, a),       # 0.0–1.0, default grey
    'emit':          True,               # optional — use Emission shader
    'emit_strength': 5.0,               # optional — emission intensity
}}
```

When `emit=False` (default): Principled BSDF is used (solid, realistic).
When `emit=True`: Emission shader is used (glowing, neon, stars, plasma).

> **Eevee bloom required for emission glow.** Call `configure_eevee` first
> so the bloom post-process makes emissive materials visibly glow.

---

### assign_material

Assign a previously created material to an object.

```python
{'cmd': 'assign_material', 'args': {
    'object':   'ObjectName',
    'material': 'MaterialName',
}}
```

In Blender: uses `obj.data.materials.append(mat)` — the only valid API.
In mock: appends to `obj.material_slots` list.

---

### set_material_color

Change the base colour of an existing material.

```python
{'cmd': 'set_material_color', 'args': {
    'name':  'MaterialName',
    'color': (r, g, b, a),
}}
```

---

## Cameras

### create_camera

Create a camera and automatically set it as the active scene camera.

```python
{'cmd': 'create_camera', 'args': {
    'name':     'CameraName',
    'location': (x, y, z),   # optional, default (0,0,5)
}}
```

In Blender: calls `bpy.ops.object.camera_add()` and assigns
`bpy.context.scene.camera = obj`.

---

### set_camera_target

Make the camera always look at a fixed point by adding a **Track To**
constraint. The camera's position can be animated freely — the constraint
keeps it pointed at the target throughout.

```python
{'cmd': 'set_camera_target', 'args': {
    'name':   'CameraName',
    'target': (x, y, z),   # world-space point to look at
}}
```

In Blender: creates an Empty at `target`, then adds a `TRACK_TO` constraint
(`track_axis='TRACK_NEGATIVE_Z'`, `up_axis='UP_Y'`) to the camera.
In mock: no-op (returns success).

---

### set_focal_length

Set the camera's lens focal length in millimetres.

```python
{'cmd': 'set_focal_length', 'args': {
    'name':         'CameraName',
    'focal_length': 50.0,
}}
```

---

### set_depth_of_field

Configure depth-of-field blur.

```python
{'cmd': 'set_depth_of_field', 'args': {
    'name':           'CameraName',
    'enabled':        True,
    'focus_distance': 10.0,
    'fstop':          2.8,
}}
```

---

## Lights

### create_light

Create a light with optional colour and energy, set in one command.

```python
{'cmd': 'create_light', 'args': {
    'name':     'LightName',
    'type':     'POINT|SUN|SPOT|AREA',
    'location': (x, y, z),
    'color':    (r, g, b),      # RGB only — no alpha
    'energy':   1000.0,         # watts (Blender 4.x) or arbitrary (3.x)
}}
```

In Blender: calls `bpy.ops.object.light_add(type=..., location=...)`.

---

### set_light_energy

Adjust intensity of an existing light.

```python
{'cmd': 'set_light_energy', 'args': {
    'name':   'LightName',
    'energy': 5000.0,
}}
```

---

### set_light_color

Set the RGB colour of an existing light.

```python
{'cmd': 'set_light_color', 'args': {
    'name':  'LightName',
    'color': (r, g, b),
}}
```

---

### set_light_type

Change the type of an existing light.

```python
{'cmd': 'set_light_type', 'args': {
    'name': 'LightName',
    'type': 'POINT|SUN|SPOT|AREA',
}}
```

---

## World & Render

### set_world_background

Set the world background to a solid colour.

```python
{'cmd': 'set_world_background', 'args': {
    'color': (r, g, b),    # 3-component, default dark grey
}}
```

In Blender: configures `world.node_tree.nodes["Background"]`.

---

### create_space_world

Build a space world shader: pure black background + procedural Voronoi
starfield baked into the world node tree. No individual star objects — the
entire starfield costs zero scene-object overhead.

```python
{'cmd': 'create_space_world', 'args': {
    'star_density':   350,    # Voronoi scale → more = more stars
    'star_brightness': 2.5,  # emission strength of visible stars
}}
```

Node chain: `TexCoord → Voronoi(F1) → Subtract(1−x) → Power(^30) → MixShader`

In mock: no-op (returns success).

---

### configure_eevee

Switch to Eevee as the render engine and configure bloom and sample count.
**Call this before creating any emissive materials** — bloom is what makes
emission visible in the viewport and in renders.

```python
{'cmd': 'configure_eevee', 'args': {
    'width':   1280,   # render resolution X
    'height':  720,    # render resolution Y
    'samples': 16,     # taa_render_samples (lower = faster)
}}
```

Bloom properties (`use_bloom`, `bloom_threshold`, etc.) apply to Blender 3.x
Eevee. On Blender 4.x Eevee Next these properties are skipped silently —
use the compositor's Glare node for bloom instead.

In mock: no-op (returns success).
