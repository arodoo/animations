---
description: 
---

Rol: Eres un Arquitecto de Software experto en Python y Automatización.

Contexto: Estoy construyendo un motor de animación procedural en Blender (bpy). Necesito la "semilla" del sistema: el mecanismo central que traduce instrucciones de texto plano (datos) en ejecuciones de código (acción).

El Reto: Necesito implementar un patrón de Dynamic Dispatch (Despacho Dinámico). El sistema recibirá una lista de instrucciones abstractas (ej: {'cmd': 'crear_actor', 'args': {...}}). El sistema debe encontrar automáticamente la función correspondiente y ejecutarla.

Tu Tarea: Escribe el script de Python más óptimo, limpio y extensible para resolver este problema.

Tus Decisiones (Libertad total): Tú decides la implementación técnica. ¿Es mejor usar un diccionario de mapeo manual? ¿Es mejor usar decoradores (@register_command) para autodescubrimiento de funciones? ¿Es mejor usar introspección (getattr)? Elige la opción que minimice la fricción para agregar nuevos comandos en el futuro.

Requisitos:

El Núcleo: Un bucle que procese una lista de datos y ejecute ciegamente.

La Prueba: Implementa 2 comandos básicos (spawn_primitive, move_object) para demostrar que el despacho funciona.

Cero Hardcoding: El bucle principal NO debe tener if/elif gigantes. Debe ser agnóstico al comando.

Al finalizar, Crea tests/mocks/bpy_mock.py:

No quiero stubs vacíos. Quiero clases funcionales mínimas.

Implementa Context, Data, Objects, y Object.

Comportamiento Requerido:

bpy.data.objects.new(name, mesh): Debe crear una instancia de clase Object y guardarla en un diccionario interno.

obj.location: Debe ser un vector (x,y,z) que yo pueda leer y escribir.

obj.keyframe_insert("location", frame=10): Debe guardar ese valor en un diccionario interno obj.animation_data.

Crea el bridge.py:

El script que intenta importar bpy real, y si falla (ImportError), carga tu bpy_mock.

Crea la Semilla de Lógica (core/logic.py):

Una función crear_escena_prueba() que use el bridge.bpy para crear un cubo y moverlo.

Crea el Test (test_runner.py):

Un script que ejecute crear_escena_prueba() y luego imprima:

"Objetos en escena: [Nombre]"

"Posición final: (X, Y, Z)"

"Keyframes guardados: {frame: valor}"

Objetivo Final: Quiero copiar tu código, pegarlo en mi VSCode, darle "Run" en la terminal (sin Blender) y ver en la consola que el cubo se creó y se "movió" matemáticamente, .además, ten en cuenta que la arquitectura debe ser extensible para soportar en el futuro: deformaciones de malla (para bordes redondos o expresiones), jerarquías complejas (rigging de extremidades), sincronización labial (lipsync con audio), y propiedades avanzadas de entorno como simulaciones físicas (ropa, colisiones, gravedad), sistemas de partículas (polvo, lluvia, abstracciones), cinematografía óptica (profundidad de campo, cambio de lentes) y post-procesado (bloom, motion blur). El sistema no debe romperse al añadir estas capas de complejidad sobre la base simple.@GEMINI.md .
# ** nota adicional: ** quiero mínimo 20 e2e pruebas del sistema, complejas de distintos casos de usos, deben de pasar el 100% de ellas