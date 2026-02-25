# Quasar Black Hole: Troubleshooting & Resolved Issues

This document records the technical challenges encountered during the development of the Quasar Black Hole scene and their respective solutions.

---

## 1. JetSouth Invisibility Issues

During initial renders, the South (receding) jet was completely invisible or appeared only as a non-glowing "white tube." This was caused by three overlapping issues:

### A. Massive Brightness Disparity (Doppler Beaming)
**Problem:** The `JetNorth` emission was boosted by the relativistic Doppler factor ($D^3$), while `JetSouth` used the base emission. For $\Gamma=7$, this created a ~2,740x brightness difference.
**Solution:** Artificially matched the `JetSouth` emission strength to `JetNorth` in `_bh_jets.py`. color (orange-red vs. blue) remains the primary indicator of recession.

### B. Material Slot Blocking ("White Tube" Bug)
**Problem:** Blender's `primitive_cylinder_add` automatically assigns a default grey material to Slot 0. The `assign_material` command was appending our custom material to Slot 1, which the mesh ignored in the viewport.
**Solution:** Modified `assign_material` in `app/commands/scene/materials.py` to explicitly overwrite Slot 0 if it exists.

### C. Back-face Culling
**Problem:** The `JetSouth` mesh normals point towards $-Z$. When viewed from the $+Z$ hemisphere (above), the camera sees the "interior" faces. Blender's Eevee engine culled these faces by default.
**Solution:** Disabled back-face culling on all emission materials by setting `mat.use_backface_culling = False`.

---

## 2. Scene Occlusion by Cartesian Grid

**Problem:** The `CartesianGrid` plane was initially placed at $Z = -0.001$. As a solid, opaque mesh, it acted as a "floor" that completely blocked any geometry in the negative $Z$ space (like the `JetSouth`) when viewed from above.

**Solution:**
1.  **Repositioning:** the grid was moved to $Z = -80$, well below all scene geometry (the jet tip is at $Z \approx -43$).
2.  **Transparency:** enabled bidirectional rendering (`use_backface_culling = False`) so the grid itself is visible from underneath if the camera orbits into the negative $Z$ hemisphere.

---

## 3. Camera Grouping & Distancing

**Problem:** Standard orbital radius (150 BU) was too tight for the high-quality quasar scene including the new grid and jet knots.
**Solution:** Increased `_CAM_RADIUS` to 240 BU (+60%) in `_cam.py` to provide a more cinematic wide shot that captures both poles and the grid reference.

---

## Preventive Measures for Future Scenes

1.  **Material Assignment:** always ensure we are targeting the primary material slot (Slot 0) for primitive meshes.
2.  **Scene Depth:** avoid placing "floor" objects at $Z=0$ if the scene has symmetric geometry above and below the plane.
3.  **Back-face Culling:** for volumetric or thin emissive objects (jets, rings), always disable back-face culling to ensure visibility from all possible camera angles.
