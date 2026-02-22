Quasar BH scene — project layout

This folder contains the quasar black hole scene and helpers.

Structure (intended):
- assets/       : textures, billboard sprites, external assets
- materials/    : reusable material definitions and presets
- animations/   : animation-specific helpers and exports
- docs/         : scene-specific notes and tuning guide

Notes:
- Existing scene modules remain at the package root for compatibility.
- Add material presets or billboard textures into `assets/` and create
  helper loaders in `materials/` that register materials via the
  `app.commands.create_material` command.
