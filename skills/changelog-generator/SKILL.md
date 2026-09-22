---
name: changelog-generator
description: "Changelog or release notes from git history. \"genera el changelog\", \"notas de la versión\", \"qué cambió desde la última release\"."
---

# Changelog-Generator — traducir commits a consecuencias para quien usa

## Overview

Un changelog no es un volcado de commits: es la respuesta a **"¿qué cambia para mí?"**. El lector no sabe qué es `refactor(core): extract session handler`; sí entiende "las sesiones ya no se pierden al reiniciar el servidor".

## Proceso

1. **Rango real**: desde la última etiqueta (o la fecha indicada) hasta hoy. Confírmalo antes de escribir.
2. **Leer el historial completo** del rango, incluidos los PR fusionados. Si los mensajes son pobres, mira el diff: un changelog honesto puede requerir leer código.
3. **Filtrar**: lo que no afecta a quien usa (formateo, cambios internos de pruebas, ajustes de CI) va a una sección aparte o se omite, no se infla la lista.
4. **Agrupar por impacto**, no por autor ni por rama.
5. **Reescribir en lenguaje de usuario**: qué puede hacer ahora, qué se arregló, qué dejó de funcionar.
6. **Destacar lo que rompe compatibilidad** al principio, con la acción necesaria para migrar. Es la única parte que el lector no puede saltarse.

## Formato

```markdown
## [<versión>] - <YYYY-MM-DD>

### Rompe compatibilidad
- <qué cambió, qué hay que hacer para migrar>

### Añadido
- <funcionalidad nueva, en términos de lo que el usuario puede hacer>

### Cambiado
- <comportamiento distinto y por qué importa>

### Arreglado
- <el síntoma que el usuario sufría, no el nombre de la función corregida>

### Seguridad
- <vulnerabilidad corregida y si requiere acción>

### Interno
- <solo si el público son desarrolladores del proyecto>
```

## Reglas

- **Nada que no esté en el historial.** Si un cambio no aparece en los commits, no se inventa: se pregunta.
- Nombra el síntoma, no la implementación: "los reportes ya no se duplican al reintentar" antes que "se agregó clave de idempotencia en `report_service`".
- Enlaza incidencias o PR cuando existan.
- Lo que rompe compatibilidad **siempre** primero y con instrucciones de migración.
- Menciona cambios en requisitos: versión mínima del runtime, variables nuevas obligatorias, migraciones de datos necesarias.
- Si el proyecto usa versionado semántico, verifica que el salto de versión corresponda al contenido (algo que rompe compatibilidad no puede ser un parche).
- Una lista de 60 puntos no la lee nadie: agrupa lo menor.

## Anti-racionalización

| Excusa | Realidad |
|---|---|
| "Copio los mensajes de commit y listo" | Los commits hablan de código; el changelog habla de consecuencias. |
| "No pongo lo que rompe compatibilidad para no asustar" | Asusta más descubrirlo en producción. Es la sección más importante. |
| "Agrego un par de mejoras que seguro entraron" | Si no está en el historial, no existió. Pregunta. |
| "El changelog lo hago al final del trimestre" | Se escribe con el contexto fresco, o se escribe mal. |

## Formato de salida

`CHANGELOG.md` actualizado (formato Keep a Changelog), el rango de commits usado, y la lista de cambios que se omitieron por no afectar a quien usa.
