Quasar BH scene — project layout and camera guidance

This folder contains the quasar black hole scene and helpers. The scene
is intended as a reusable factory: small focused modules produce commands
that are dispatched to the Blender bridge so scenes can be generated
programmatically or executed in the Blender text editor.

Structure (intended):
- assets/       : textures, billboard sprites, external assets
- materials/    : reusable material definitions and presets
- animations/   : animation-specific helpers and exports
- docs/         : scene-specific notes and tuning guide

Camera & Composition — Do / Don't
- Do: orbit the camera around the center (panoramic sweep) rather than
  holding it on the polar axis. A panoramic orbit reveals the disk and
  the singularity from many angles.
- Do: use an off-axis top-down angle (e.g., 30°–55° elevation) so the
  jets are visible but the camera is not placed directly on the jet axis.
- Do: prefer a telephoto focal length (50–120 mm) to compress depth and
  emphasize the central singularity. Use a low `fstop` for DOF on final
  renders to draw attention to the inner disk.
- Do: add a brief, subtle dolly-in (close pass) near the mid-point of the
  animation to reveal inner structure — avoid aiming the dolly exactly
  along the jet axis.

- Don't: place the camera straight above the system on the +Z or -Z axis
  during long shots — this hides the singularity inside the jet cone.
- Don't: use extremely wide angles for final shots when you want to
  highlight the singularity — use wide only for establishing/context shots.

Visuals & Render — Do / Don't (quick)
- Do: use Physically-Based Rendering (Principled BSDF) and subtle noise
  maps for ring detail. Use emissive shaders for hot inner rings and
  bloom/glare in compositor for glow.
- Do: render final frames in Cycles with denoising; use Eevee for fast
  previews and iteration but test final look in Cycles.
- Don't: render jet particles as screen-space halos for final delivery;
  prefer instanced billboards or small geometry with motion blur for
  streaking.

Notes:
- The codebase provides modular builders under `animations/` and
  presets under `materials/` so you can tune camera, jets, disk, and
  materials independently.
- To iterate quickly inside Blender, use the launcher which purges
  cached bytecode and reimports modules so each run picks up file edits.
