---
description: Steps to create a new animation
---

---
description: Create a highly scalable, parametric Blender animation following DDD and Factory principles.
---

# Animation Factory Workflow

Sigue estrictamente estos pasos y principios para escalar la fábrica de animaciones y asegurar calidad "Premium" sin destruir código previo:

## 1. Principios de Arquitectura (DDD Inquebrantable)
- **Límite 120/80 (CI)**: MAX 120 líneas por archivo, 80 caracteres/línea. Si un [_builder.py](cci:7://file:///d:/zProyectos/01Python/animations/app/components/camera_builder.py:0:0-0:0) crece, divídelo semánticamente en componentes ([_materials.py](cci:7://file:///d:/zProyectos/01Python/animations/scenes/math_sets/animations/_materials.py:0:0-0:0), `_strobe.py`, `_logic.py`). ¡Cero excepciones!
- **Idempotencia (Escenarios Aislados)**: Toda nueva idea vive en un dominio separado (ej. `scenes/<nueva_escena>/`). JAMÁS modifiques una escena que ya funciona para acomodar código de otra.
- **La Barrera API (C-API vs Python)**: Usa comandos del `Dispatcher` ([spawn_primitive](cci:1://file:///d:/zProyectos/01Python/animations/app/commands/objects/spawn_primitive.py:33:0-118:5)). Protege los constructores de bajo nivel (`bpy.ops.*`) usando *Whitelists* de parámetros matemáticos puros. Aplica la estética (`shade_smooth`) después, como modificadores.

## 2. Componentes de Fábrica (Reutilización)
- **NO reinventes la rueda**: Antes de crear esferas o anillos con primitivas crudas, busca en `app/components/`. Usa fábricas perfeccionadas como `build_celestial_body()` o `build_dyson_sphere()`.

## 3. Dinamismo y Calidad Visual ("Wow Effect")
- **El Vacío Atrapa la Vista**: Usa fondos oscuros (`[0.005, 0.005, 0.005]`) y contrastes marcados (emisores altos vs metales `emit_strength: 0.8 / roughness 0.25`).
- **NADA ESTÁ ESTÁTICO (Caos Cinético)**: Un objeto en pantalla siempre debe estar "vivo". Usa parámetros de frame (`t = f / 30.0`) inyectando funciones seno/coseno para generar flotaciones (`hover_z`) y micronúcleos de rotación invisibles pero constantes.
- **Varianza Matemática (Desincronización)**: Al animar colecciones, rompe la uniformidad multiplicando las velocidades por el índice del objeto (`speed_mult = 1.0 + (i * 0.6)`).
- **Z-Fighting Cero**: Al apilar geometrías concéntricas, usa bucles matemáticos con suma de `clearance` para imposibilitar empalmes espaciales.

## 4. Orquestación y Ejecución
1. El archivo maestro siempre despacha baterías de comandos: `results = dispatch_batch(batch)`.
2. Las pruebas lógicas y matemáticas se corren con `pytest` externamente.
3. **RENDERIZADO OBLIGATORIO EN BLENDER**: Inyectar `import bpy` desde una terminal externa fallará por diseño.  Para renderizar, abre `scenes/<nueva_escena>/launcher.py` dentro de la pestaña "Scripting" de Blender y usa "Run Script".
